"""Functions to export data into different file formats and organizations.

To allow datman to export to a new format make a subclass of SessionExporter
or SeriesExporter depending on whether the new format requires data from
a complete scan session or a single series, respectively. The new subclass
should implement all abstract methods, including 'export' which does the
actual work of generating outputs.

Also, ensure that subclasses define the 'type' attribute to be a short
unique key that can be referenced in config files (e.g. 'nii').
"""
from abc import ABC, abstractmethod
from datetime import datetime
from glob import glob
import logging
import os
import re

import pydicom as dicom

import datman.dashboard
from datman.exceptions import UndefinedSetting, DashboardException
from datman.scanid import (parse_filename, parse_bids_filename, ParseException,
                           KCNIIdentifier)
from datman.utils import (run, make_temp_directory, get_extension,
                          filter_niftis, find_tech_notes, read_blacklist,
                          get_relative_source)

try:
    from dcm2bids import Dcm2bids
except ImportError:
    DCM2BIDS_FOUND = False
else:
    DCM2BIDS_FOUND = True

logger = logging.getLogger(__name__)


def get_exporter(key, scope="series"):
    """Find an exporter class for a given key identifier.

    Args:
        key (:obj:`str`): The 'type' identifier of a defined exporter (e.g.
            'nii').
        scope (:obj:`str`, optional): Whether to search for a series or session
            exporter. Defaults to 'series'.

    Returns:
        :obj:`datman.exporters.Exporter`: The Exporter subclass for the type,
            if one is defined, or else None.
    """
    if scope == "series":
        exp_set = SERIES_EXPORTERS
    else:
        exp_set = SESSION_EXPORTERS

    try:
        exporter = exp_set[key]
    except KeyError:
        logger.error(
            f"Unrecognized format {key} for {scope}, no exporters found.")
        return None
    return exporter


class Exporter(ABC):
    """An abstract base class for all Exporters.
    """

    # Subclasses must define this
    type = None

    @classmethod
    def get_output_dir(cls, session):
        """Retrieve the exporter's output dir without needing an instance.
        """
        return getattr(session, f"{cls.type}_path")

    @abstractmethod
    def outputs_exist(self):
        """Whether outputs have already been generated for this Exporter.

        Returns:
            bool: True if all expected outputs exist, False otherwise.
        """

    @abstractmethod
    def needs_raw_data(self):
        """Whether raw data must be downloaded for the Exporter.

        Returns:
            bool: True if raw data must be given, False otherwise. Note that
                False may be returned if outputs already exist.
        """

    @abstractmethod
    def export(self, raw_data_dir, **kwargs):
        """Exports raw data to the current Exporter's format.

        Args:
            raw_data_dir (:obj:`str`): The directory that contains the
                downloaded raw data.
        """

    def make_output_dir(self):
        """Creates the directory where the Exporter's outputs will be stored.

        Returns:
            bool: True if directory exists (or isn't needed), False otherwise.
        """
        try:
            os.makedirs(self.output_dir)
        except FileExistsError:
            pass
        except AttributeError:
            logger.debug(f"output_dir not defined for {self}")
        except PermissionError:
            logger.error(f"Failed to make output dir {self.output_dir} - "
                         "PermissionDenied.")
            return False
        return True


class SessionExporter(Exporter):
    """A base class for exporters that take an entire session as input.

    Subclasses should override __init__ (without changing basic input args)
    and call super().__init__(config, session, experiment, **kwargs).

    The init function for SessionExporter largely exists to define expected
    input arguments and set some universally needed attributes.
    """

    def __init__(self, config, session, experiment, dry_run=False, **kwargs):
        self.experiment = experiment
        self.dry_run = dry_run

    def __repr__(self):
        fq_name = str(self.__class__).replace("<class '", "").replace("'>", "")
        name = fq_name.rsplit(".", maxsplit=1)[-1]
        return f"<{name} - {self.experiment.name}>"


class SeriesExporter(Exporter):
    """A base class for exporters that take a single series as input.
    """

    # Subclasses should set this
    ext = None

    def __init__(self, output_dir, fname_root, echo_dict=None, dry_run=False,
                 **kwargs):
        self.output_dir = output_dir
        self.fname_root = fname_root
        self.echo_dict = echo_dict
        self.dry_run = dry_run

    def outputs_exist(self):
        return os.path.exists(
            os.path.join(self.output_dir, self.fname_root + self.ext))

    def needs_raw_data(self):
        return not self.outputs_exist()

    def __repr__(self):
        fq_name = str(self.__class__).replace("<class '", "").replace("'>", "")
        name = fq_name.rsplit(".", maxsplit=1)[-1]
        return f"<{name} - {self.fname_root}>"


class BidsExporter(SessionExporter):
    """An exporter that runs dcm2bids.
    """

    type = "bids"

    def __init__(self, config, session, experiment, bids_opts=None, **kwargs):
        self.exp_label = experiment.name
        self.bids_sub = session._ident.get_bids_name()
        self.bids_ses = session._ident.timepoint
        self.bids_folder = session.bids_root
        self.output_dir = session.bids_path
        self.keep_dcm = bids_opts.keep_dcm if bids_opts else False
        self.force_dcm2niix = bids_opts.force_dcm2niix if bids_opts else False
        self.clobber = bids_opts.clobber if bids_opts else False
        self.log_level = bids_opts.log_level if bids_opts else "INFO"
        self.dcm2bids_config = bids_opts.dcm2bids_config if bids_opts else None
        super().__init__(config, session, experiment, **kwargs)

    def _get_scan_dir(self, download_dir):
        return os.path.join(download_dir, self.exp_label, "scans")

    def outputs_exist(self):
        # Can't get more granular than this at the moment
        if os.path.exists(self.output_dir):
            if self.clobber:
                logger.info(
                    f"{self.output_dir} will be overwritten due to "
                    "clobber option.")
                return False
            logger.info("(Use --clobber to overwrite)")
            return True
        return False

    def needs_raw_data(self):
        return not self.outputs_exist()

    def export(self, raw_data_dir, **kwargs):
        if self.outputs_exist():
            return

        if not DCM2BIDS_FOUND:
            logger.info(f"Unable to export to {self.output_dir}, "
                        "Dcm2Bids not found.")
            return

        if self.dry_run:
            logger.info(f"Dry run: Skipping bids export to {self.output_dir}")
            return

        self.make_output_dir()

        input_dir = self._get_scan_dir(raw_data_dir)
        try:
            dcm2bids_app = Dcm2bids(
                input_dir,
                self.bids_sub,
                self.dcm2bids_config,
                output_dir=self.bids_folder,
                session=self.bids_ses,
                clobber=self.clobber,
                forceDcm2niix=self.force_dcm2niix,
                log_level=self.log_level
            )
            dcm2bids_app.run()
        except Exception as exc:
            logger.error(
                f"Dcm2Bids failed to run for {self.output_dir}. "
                f"{type(exc)}: {exc}"
            )


class NiiLinkExporter(SessionExporter):
    """Populates a study's nii folder with symlinks pointing to the bids dir.
    """

    type = "nii_link"
    ext = ".nii.gz"

    def __init__(self, config, session, experiment, **kwargs):
        self.output_dir = session.nii_path
        self.config = config
        self.tags = config.get_tags(site=session.site)
        self.bids_path = session.bids_path
        super().__init__(config, session, experiment, **kwargs)

        self.dm_names = self.get_dm_names()
        self.bids_names = self.get_bids_niftis()
        self.name_map = self.match_dm_to_bids(self.dm_names, self.bids_names)

    def get_dm_names(self):
        """Get the datman-style scan names for an entire XNAT experiment.

        Returns:
            :obj:`dict`: A dictionary of datman-style scan names for the
                session, organized by tag.
        """
        name_map = {}
        for scan in self.experiment.scans:
            for idx, name in enumerate(scan.names):
                name_map.setdefault(scan.tags[idx], []).append(name)
        return name_map

    def get_bids_niftis(self):
        """Get all nifti files from a BIDS session.

        Returns:
            :obj:`list`: A list of full paths (minus the file extension) to
                each bids format nifti file in the session.
        """
        bids_niftis = []
        for path, _, files in os.walk(self.bids_path):
            niftis = filter_niftis(files)
            for item in niftis:
                basename = item.replace(get_extension(item), "")
                bids_niftis.append(os.path.join(path, basename))
        return bids_niftis

    def match_dm_to_bids(self, dm_names, bids_names):
        """Match each datman file name to its BIDS equivalent.

        Returns:
            :obj:`dict`: A dictionary matching the intended datman file name to
                the full path (minus extension) of the same series in the bids
                folder.
        """
        name_map = {}
        for tag in dm_names:
            try:
                bids_conf = self.tags.get(tag)['Bids']
            except KeyError:
                logger.info(f"No bids config found for tag {tag}. Can't match "
                            "bids outputs to a datman-style name.")
                continue

            matches = self._find_matching_files(bids_names, bids_conf)

            if bids_conf.get('class') == 'fmap' and bids_conf.get('match_str'):
                self._add_fmap_names(
                    dm_names[tag], matches, bids_conf.get('match_str'),
                    name_map)
                continue

            try:
                bids_files = sorted(
                    matches,
                    key=lambda x: int(parse_bids_filename(x).run)
                )
            except ParseException:
                logger.error(
                    f"Invalid bids file name found for {self.experiment.name}."
                    f" Skipping datman nifti links for {tag}.")
                continue

            try:
                dm_files = sorted(
                    dm_names[tag],
                    key=lambda x: int(parse_filename(x)[2])
                )
            except ParseException:
                logger.error(
                    "Invalid datman file name found for "
                    f"{self.experiment.name}. Skipping datman nifti links for "
                    f"{tag}")
                continue

            for idx, item in enumerate(dm_files):
                if idx >= len(bids_files):
                    continue
                name_map[item] = bids_files[idx]

        return name_map

    def _find_matching_files(self, bids_names, bids_conf):
        """Search a list of bids files to find series that match a datman tag.

        Args:
            :obj:`list`: A list of bids file names to search through.
            :obj:`dict`: The bids configuration for a single tag from datman's
                configuration files.

        Returns:
            :obj:`list`: A list of full paths (minus extension) of bids files
                that match the tag configuration. If none match, an empty
                list will be returned.
        """
        matches = self._filter_bids(
            bids_names, bids_conf.get('class'), par_dir=True)
        matches = self._filter_bids(
            matches, bids_conf.get(self._get_label_key(bids_conf)))
        matches = self._filter_bids(matches, bids_conf.get('task'))
        return matches

    def _filter_bids(self, niftis, search_term, par_dir=False):
        """Find the subset of file names that matches a search string.

        Args:
            niftis (:obj:`list`): A list of nifti file names to search through.
            search_term (:obj:`str`): The search term nifti files must match.
            par_dir (bool, optional): Restricts the search to the nifti file's
                parent directory, if full paths were given.

        Returns:
            list: A list of all files that match the search term.
        """
        if not search_term:
            return niftis.copy()

        if not isinstance(search_term, list):
            search_term = [search_term]

        result = set()
        for item in niftis:
            if par_dir:
                fname = os.path.split(os.path.dirname(item))[1]
            else:
                fname = os.path.basename(item)

            for term in search_term:
                if term in fname:
                    result.add(item)
        return list(result)

    def _get_label_key(self, bids_conf):
        """Return the name for the configuration's label field.
        """
        for key in bids_conf:
            if 'label' in key:
                return key
        return ""

    def _add_fmap_names(self, dm_fmaps, bids_fmaps, match_map, name_map):
        """Add datman to BIDS filename mappings for field maps.

        Args:
            dm_fmaps (:obj:`list`): A list of datman-style field map file
                names.
            bids_fmaps (:obj:`list`): A list of BIDS file names that
                match the datman field map tag.
            match_map (:obj:`dict`): The 'match_str' field of the bids
                configuration. Used to map datman field maps to BIDS
                file names.
            name_map (:obj:`dict`): The dictionary holding the datman to
                bids name map that is being constructed. Field maps
                will be added to this dictionary.
        """
        matches = self._get_matching_fmaps(dm_fmaps, bids_fmaps, match_map)

        for dm_root, bids_files in matches.items():
            for found_bids in bids_files:
                dm_name = self._modify_dm_name(dm_root, found_bids)
                name_map[dm_name] = found_bids

    def _get_matching_fmaps(self, dm_fmaps, bids_fmaps, match_map):
        """Find BIDS file names that match datman field map names.

        Args:
            dm_fmaps (:obj:`list`): A list of datman-style field map file
                names.
            bids_fmaps (:obj:`list`): A list of BIDS file names that
                match the datman field map tag.
            match_map (:obj:`dict`): The 'match_str' field of the bids
                configuration. Used to map datman field maps to BIDS
                file names.

        Returns:
            :obj:`dict`: A mapping of datman scan names to their BIDS
                format equivalent.
        """
        matches = {}
        for fmap in bids_fmaps:
            bids_file = parse_bids_filename(fmap)
            if bids_file.acq not in match_map:
                logger.debug(
                    "Tag settings can't match bids acquisition to datman "
                    f"name for: {bids_file}")
                continue

            for nii_file in dm_fmaps:
                _, _, _, description = parse_filename(nii_file)
                terms_match = [search_term in description
                               for search_term in match_map[bids_file.acq]]

                if any(terms_match):
                    matches.setdefault(nii_file, []).append(fmap)

        return matches

    def _modify_dm_name(self, dm_name, bids_name):
        """Modify a datman-style field map name's description.

        BIDS format often splits the field maps in two. To make links for these
        in the nifti folder the description must be modified to give each a
        unique file name.

        Args:
            dm_name (:obj:`str`): A datman style file name root that will
                be modified.
            bids_name (:obj:`str`): The BIDS style file name for the series.

        Returns:
            str: A datman style file name with a modified series description.
        """
        ident = parse_bids_filename(bids_name)
        new_descr = []
        if ident.dir:
            new_descr.append(f"dir-{ident.dir}")
        if ident.run:
            new_descr.append(f"run-{ident.run}")
        if ident.suffix:
            new_descr.append(ident.suffix)
        return dm_name + "_".join(new_descr)

    @classmethod
    def get_output_dir(cls, session):
        return session.nii_path

    def outputs_exist(self):
        for dm_name in self.name_map:
            bl_entry = read_blacklist(scan=dm_name, config=self.config)
            if bl_entry:
                continue
            full_path = os.path.join(self.output_dir, dm_name + self.ext)
            if not os.path.exists(full_path):
                return False
        return True

    def needs_raw_data(self):
        return False

    def export(self, *args, **kwargs):
        # Re run this before exporting, in case new BIDS files exist.
        self.bids_names = self.get_bids_niftis()
        self.name_map = self.match_dm_to_bids(self.dm_names, self.bids_names)

        if self.dry_run:
            logger.info("Dry run: Skipping making nii folder links for "
                        f"mapping {self.name_map}")
            return

        self.make_output_dir()
        for dm_name, bids_name in self.name_map.items():
            self.make_link(dm_name, bids_name)

    def make_link(self, dm_file, bids_file):
        """Create a symlink in the datman style that points to a bids file.

        Args:
            dm_file (:obj:`str`): A valid datman file name.
            bids_file (:obj:`str`): The full path to a bids file (minus
                extension.)
        """
        base_target = os.path.join(self.output_dir, dm_file)
        if read_blacklist(scan=base_target, config=self.config):
            logger.debug(f"Ignoring blacklisted scan {dm_file}")
            return

        for source in glob(bids_file + '*'):
            ext = get_extension(source)
            target = base_target + ext
            rel_source = get_relative_source(source, target)
            try:
                os.symlink(rel_source, target)
            except FileExistsError:
                pass
            except Exception as exc:
                logger.error(f"Failed to create {target}. Reason - {exc}")


class DBExporter(SessionExporter):
    """Add a datman-style session and its contents to datman's QC dashboard.
    """

    type = "db"

    def __init__(self, config, session, experiment, **kwargs):
        try:
            study_resource_dir = config.get_path("resources")
        except UndefinedSetting:
            study_resource_dir = ""

        try:
            resources_dir = os.path.join(
                config.get_path("resources"),
                session._ident.get_full_subjectid_with_timepoint_session()
            )
        except UndefinedSetting:
            resources_dir = ""

        self.nii_path = session.nii_path
        self.output_dir = None
        self.ident = session._ident
        self.study_resource_path = study_resource_dir
        self.resources_path = resources_dir
        self.date = experiment.date
        self.names = self.get_scan_names(session, experiment)
        super().__init__(config, session, experiment, **kwargs)

    def get_scan_names(self, session, experiment):
        """Gets list of datman-style scan names for a session.

        Returns:
            :obj:`dict`: A dictionary of datman style scan names mapped to
                the bids style name if one can be found, otherwise, an
                empty string.
        """
        names = {}
        # use experiment.scans, so dashboard can report scans that didnt export
        for scan in experiment.scans:
            # If outputs exist, get the mangled name instead.
            for name in self.get_final_names(scan):
                names[name] = self.get_bids_name(name, session)
        return names

    def get_final_names(self, scan):
        """Gets the file name as it appears in 'nii' dir.

        Some files (namely field maps) undergo some mangling during export.
        This will grab the mangled names if they exist.

        Returns:
            :obj:`list`: A list of all datman-style scan names with
                modifications (if any) applied.
        """
        # Return the actual names that sessions were exported to
        altered_names = []
        for name in scan.names:
            found = glob(os.path.join(self.nii_path, name + "*.nii.gz"))
            if not found:
                altered_names.append(name)
            else:
                for full_path in found:
                    fname = os.path.basename(full_path)
                    stem = fname.replace(get_extension(fname), "")
                    altered_names.append(stem)

        return altered_names

    def get_bids_name(self, dm_name, session):
        """Get BIDS style scan name from a datman style nifti.

        Returns:
            str: A valid bids style file name or an empty string if one
                cannot be found.
        """
        found = [item for item in session.find_files(dm_name)
                 if ".nii.gz" in item]
        if not found or not os.path.islink(found[0]):
            return ""
        bids_src = os.readlink(found[0])
        bids_name = os.path.basename(bids_src)
        return bids_name.replace(get_extension(bids_name), "")

    def export(self, *args, **kwargs):
        if self.dry_run:
            logger.info("Dry run: Skipping database update for "
                        f"{str(self.ident)}")
            return

        if not datman.dashboard.dash_found:
            logger.warning("Dashboard database not found, unable to add "
                           f"{str(self.ident)} and its contents.")
            return

        session = self.make_session()

        if not session.tech_notes and session.expects_notes():
            self.add_tech_notes(session)

        for file_stem in self.names:
            self.make_scan(file_stem)

    def outputs_exist(self):
        try:
            session = datman.dashboard.get_session(self.ident)
        except DashboardException:
            return False
        except ParseException:
            logger.error(
                f"Session name {self.ident} is not datman format. Ignoring.")
            return True

        if not session:
            return False

        for name in self.names:
            try:
                scan = datman.dashboard.get_scan(name)
            except DashboardException:
                return False
            except ParseException:
                logger.error(
                    f"Scan name {name} is not datman format. Ignoring.")
                continue

            if not scan:
                return False

        return True

    @classmethod
    def get_output_dir(cls, session):
        return None

    def needs_raw_data(self):
        return False

    def make_session(self):
        """Add the current session to datman's QC database.

        Returns:
            :obj:`dashboard.models.Session`: The created scan session or None.
        """
        logger.debug(f"Adding session {str(self.ident)} to dashboard.")
        try:
            session = datman.dashboard.get_session(self.ident, create=True)
        except datman.dashboard.DashboardException as exc:
            logger.error(f"Failed adding session {str(self.ident)} to "
                         f"database. Reason: {exc}")
            return None

        self._set_alt_ids(session)
        self._set_date(session)

        return session

    def _set_alt_ids(self, session):
        """Add alternate ID formats for the scan session to the database.

        Args:
            session (:obj:`dashboard.models.Session`): A valid QC dashboard
                scan session.
        """
        session.timepoint.bids_name = self.ident.get_bids_name()
        session.timepoint.bids_session = self.ident.timepoint
        session.save()

        if not isinstance(self.ident, KCNIIdentifier):
            return

        session.timepoint.kcni_name = self.ident.get_xnat_subject_id()
        session.kcni_name = self.ident.get_xnat_experiment_id()
        session.save()
        return

    def _set_date(self, session):
        """Add the scan date for a scan session to the QC database.

        Args:
            session (:obj:`dashboard.models.Session`): A valid QC dashboard
                scan session.
        """
        if not self.date:
            logger.debug(f"No scan date found for {str(self.ident)}, "
                         "leaving blank.")
            return

        try:
            date = datetime.strptime(self.date, '%Y-%m-%d')
        except ValueError:
            logger.error(f"Invalid scan date {self.date} for session "
                         f"{str(self.ident)}")
            return

        if date == session.date:
            return

        session.date = date
        session.save()

    def add_tech_notes(self, session):
        """Add the path to a scan session's tech notes to the database.

        Args:
            session (:obj:`dashboard.models.Session`): A valid QC dashboard
                scan session.
        """
        notes = find_tech_notes(self.resources_path)
        if not notes:
            logger.debug(f"No tech notes found in {self.resources_path}")
            return

        # Store only the path relative to the resources dir
        session.tech_notes = notes.replace(
            self.study_resource_path, "").lstrip("/")
        session.save()

    def make_scan(self, file_stem):
        """Add a single scan to datman's QC dashboard.

        Args:
            file_stem (:obj:`str`): A valid datman-style file name.
        """
        logger.debug(f"Adding scan {file_stem} to dashboard.")
        try:
            scan = datman.dashboard.get_scan(file_stem, create=True)
        except datman.dashboard.DashboardException as exc:
            logger.error(f"Failed adding scan {file_stem} to dashboard "
                         f"with error: {exc}")
            return

        self._add_bids_scan_name(scan, file_stem)
        self._add_side_car(scan, file_stem)
        self._add_conversion_errors(scan, file_stem)

    def _add_bids_scan_name(self, scan, dm_stem):
        """Add a bids format file name to a series in the QC database.

        Args:
            scan (:obj:`dashboard.models.Scan`): A QC dashboard scan.
            dm_stem (:obj:`str`): A valid bids format scan name, or an
                empty string if the update should be skipped.
        """
        bids_stem = self.names[dm_stem]
        if not bids_stem:
            return

        try:
            bids_ident = parse_bids_filename(bids_stem)
        except ParseException:
            logger.debug(f"Failed to parse bids file name {bids_stem}")
            return
        scan.add_bids(str(bids_ident))

    def _add_side_car(self, scan, file_stem):
        """Add the JSON side car contents to the QC database.

        Args:
            scan (:obj:`dashboard.models.Scan`): A QC dashboard scan.
            file_stem (:obj:`str`): A valid datman-style file name. Used to
                find the json side car file.
        """
        nii_file = self._get_file(file_stem, ".nii.gz")
        if not nii_file:
            # File exists on xnat but hasnt been generated.
            return

        side_car = self._get_file(file_stem, ".json")
        if not side_car:
            logger.error(f"Missing json side car for {file_stem}")
            return

        try:
            scan.add_json(side_car)
        except Exception as exc:
            logger.error("Failed to add JSON side car to dashboard "
                         f"record for {side_car}. Reason - {exc}")

    def _add_conversion_errors(self, scan, file_stem):
        """Add any dcm2niix conversion errors to the QC database.

        Args:
            scan (:obj:`dashboard.models.Scan`): A QC dashboard scan.
            file_stem (:obj:`str`): A valid datman style file name. Used to
                find the conversion error file (if one exists).
        """
        convert_errors = self._get_file(file_stem, ".err")
        if not convert_errors:
            return
        message = self._read_file(convert_errors)
        scan.add_error(message)

    def _get_file(self, fname, ext):
        """Find a file on the file system.

        Args:
            fname (:obj:`str`): A file name (minus extension).
            ext (:obj:`str`): A file extension.

        Returns:
            str: The full path to the file matching the given name and
                extension, otherwise None.
        """
        found = os.path.join(self.nii_path, fname + ext)
        if not os.path.exists(found):
            logger.debug(f"File not found {found}")
            return None
        return found

    def _read_file(self, fpath):
        """Read the contents of a file.

        Args:
            fpath (:obj:`str`): The full path to a file.

        Returns:
            str: The contents of the file or None if the file cannot be read.
        """
        try:
            with open(fpath, "r") as file_handle:
                message = file_handle.readlines()
        except Exception as exc:
            logger.debug(f"Can't read file {file_handle} - {exc}")
            return None
        return message


class NiiExporter(SeriesExporter):
    """Export a series to nifti format with datman-style names.
    """

    ext = ".nii.gz"

    type = "nii"

    def export(self, raw_data_dir, **kwargs):
        if self.dry_run:
            logger.info(f"Dry run: Skipping export of {self.fname_root}")
            return

        if self.outputs_exist():
            logger.debug(f"Outputs exist for {self.fname_root}, skipping.")
            return

        self.make_output_dir()

        with make_temp_directory(prefix="export_nifti_") as tmp:
            _, log_msgs = run(f'dcm2niix -z y -b y -o {tmp} {raw_data_dir}',
                              self.dry_run)
            for tmp_file in glob(f"{tmp}/*"):
                self.move_file(tmp_file)
                stem = self._get_fname(tmp_file)
                self.report_issues(stem, str(log_msgs))

    def move_file(self, gen_file):
        """Move the temp outputs of dcm2niix to the intended output directory.

        Args:
            gen_file (:obj:`str`): The full path to the generated nifti file
                to move.
        """
        fname = self._get_fname(gen_file)

        if not fname:
            return

        out_file = os.path.join(self.output_dir, fname)
        if os.path.exists(out_file):
            logger.info(f"Output {out_file} already exists. Skipping.")
            return

        return_code, _ = run(f"mv {gen_file} {out_file}", self.dry_run)
        if return_code:
            logger.debug(f"Moving dcm2niix output {gen_file} to {out_file} "
                         "has failed.")

    def _get_fname(self, gen_file):
        """Get the intended datman-style name for a generated file.

        Args:
            gen_file (:obj:`str`): The full path to the generated nifti file
                to move.

        Result:
            str: A string filename (with extension) or an empty string.
        """
        ext = get_extension(gen_file)
        bname = os.path.basename(gen_file)

        if self.echo_dict:
            stem = self._get_echo_fname(bname, ext)
            if stem != self.fname_root:
                # File belongs to the wrong echo, skip it
                return ""
        else:
            stem = self.fname_root
        return stem + ext

    def _get_echo_fname(self, fname, ext):
        """Get a valid datman-style file name from a multiecho file.

        Args:
            fname (:obj:`str`): A filename to parse for an echo number.
            ext (:obj:`str`): The file extension to use.

        Returns:
            str: A valid datman-style file name or an empty string if one
                cannot be made.
        """
        # Match a 14 digit timestamp and 1-3 digit series num
        regex = "files_(.*)_([0-9]{14})_([0-9]{1,3})(.*)?" + ext
        match = re.search(regex, fname)

        if not match:
            logger.error(f"Can't parse valid echo number from {fname}.")
            return ""

        try:
            echo = int(match.group(4).split('e')[-1][0])
            stem = self.echo_dict[echo]
        except Exception:
            logger.error(f"Can't parse valid echo number from {fname}")
            return ""

        return stem

    def report_issues(self, stem, messages):
        """Write an error log if dcm2niix had errors during conversion.

        Args:
            stem (:obj:`stem`): A valid datman-style file name (minus
                extension).
            messages (:obj:`str`): Error messages to write.
        """
        if self.dry_run:
            logger.info(f"DRYRUN - Skipping write of error log for {stem}")
            return

        if 'missing images' not in messages:
            # The only issue we care about currently is if files are missing
            return

        dest = os.path.join(self.output_dir, stem) + ".err"
        self._write_error_log(dest, messages)

    def _write_error_log(self, dest, messages):
        """Write an error message to the file system.

        Args:
            dest (:obj:`str`): The full path of the file to write.
            messages (:obj:`str`): Intended contents of the error log.
        """
        try:
            with open(dest, "w") as output:
                output.write(messages)
        except Exception as exc:
            logger.error(f"Failed writing dcm2niix errors to {dest}. "
                         f"Reason - {type(exc).__name__} {exc} ")


class DcmExporter(SeriesExporter):
    """Export a single dicom from a scan.
    """

    type = "dcm"
    ext = ".dcm"

    def export(self, raw_data_dir, **kwargs):
        self.make_output_dir()

        if self.echo_dict:
            self._export_multi_echo(raw_data_dir)
            return

        dcm_file = self._find_dcm(raw_data_dir)
        if not dcm_file:
            logger.error(f"No dicom files found in {raw_data_dir}")
            return

        logger.debug(f"Exporting a dcm file from {raw_data_dir} to "
                     f"{self.output_dir}")
        output = os.path.join(self.output_dir, self.fname_root + self.ext)
        run(f"cp {dcm_file} {output}", self.dry_run)

    def _find_dcm(self, raw_data_dir):
        """Find the path to a valid dicom in the given directory.

        Args:
            raw_data_dir (:obj:`str`): The full path to the directory where
                raw dicoms were downloaded for the series.

        Returns:
            str: the full path to the first readable dicom found.
        """
        for path in glob(f"{raw_data_dir}/*"):
            try:
                dicom.read_file(path)
            except dicom.filereader.InvalidDicomError:
                pass
            else:
                return path
        return ""

    def _export_multi_echo(self, raw_data_dir):
        """Find a single valid dicom for each echo in a multiecho scan.

        Args:
            raw_data_dir (:obj:`str`): The full path to the directory where
                raw dicoms were downloaded for the series.
        """
        dcm_dict = {}
        for path in glob(f"{raw_data_dir}/*"):
            try:
                dcm_file = dicom.read_file(path)
            except dicom.filereader.InvalidDicomError:
                continue
            dcm_echo_num = dcm_file.EchoNumbers
            if dcm_echo_num not in dcm_dict:
                dcm_dict[int(dcm_echo_num)] = path
            if len(dcm_dict) == len(self.echo_dict):
                break

        for echo_num, dcm_echo_num in zip(self.echo_dict.keys(),
                                          dcm_dict.keys()):
            output_file = os.path.join(self.output_dir,
                                       self.echo_dict[echo_num] + self.ext)
            logger.debug(f"Exporting a dcm file from {raw_data_dir} to "
                         f"{output_file}")
            cmd = f"cp {dcm_dict[dcm_echo_num]} {output_file}"
            run(cmd, self.dry_run)


SESSION_EXPORTERS = {
    exp.type: exp for exp in SessionExporter.__subclasses__()
}

SERIES_EXPORTERS = {
    exp.type: exp for exp in SeriesExporter.__subclasses__()
}