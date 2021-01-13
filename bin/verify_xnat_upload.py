#!/usr/bin/env python
"""Report files missing from KCNI server.

Usage:
    verify_xnat_upload.py [options] <study> <dm_project> <kcni_project>
    verify_xnat_upload.py [options] <study> <dm_project> <kcni_project> <datman_exp>

Args:
    <study>             The canonical name of the study (as in the archive)
    <dm_project>        The name of the project on our xnat server
    <kcni_project>      The name of the project on KCNI's server
    <datman_exp>        The datman ID of a specific experiment to check

Options:
    --output <path>     The path to dump the file count differences that were
                        found.
    --fix               Whether to attempt to upload missing files. [Default=False]
    --site SITE         Restrict the search to a specific site. Used when
                        multiple site codes are combined within one
                        XNAT project on TIGRLab's xnat server.
"""
import os
import urllib

from docopt import docopt
import yaml

import datman.xnat
import datman.config
import datman.scanid

xnat_user = os.getenv("XNAT_USER")
xnat_pass = os.getenv("XNAT_PASS")

dm_server = "https://xnat.imaging-genetics.camh.ca"
kcni_server = "https://xnat.camh.ca/xnat"

dm_xnat = datman.xnat.xnat(dm_server, xnat_user, xnat_pass)
kcni_xnat = datman.xnat.xnat(kcni_server, xnat_user, xnat_pass)


class ResourceFolder:

    def __init__(self, xnat_entry):
        self.entry = xnat_entry
        try:
            self.label = xnat_entry['data_fields']['label']
        except KeyError:
            self.label = 'NOLABEL'
        try:
            self.f_size = xnat_entry['data_fields']['file_size']
        except KeyError:
            self.f_size = 0
        try:
            self.f_count = xnat_entry['data_fields']['file_count']
        except KeyError:
            self.f_count = 0

    def __repr__(self):
        return f"<ResourceFolder: {self.label}>"


class ScanFolder:

    def __init__(self, series_num, xnat_entry):
        self.full_entry = xnat_entry
        self.series = series_num
        if not xnat_entry['children']:
            self.raw_entry = None
            self.f_count = 0
            self.f_size = 0
            return

        for child in xnat_entry['children']:
            if child['field'] != 'file':
                continue
            self.raw_entry = None
            for entry in child['items']:
                if ('content' not in entry['data_fields'] or
                    'SNAPSHOT' in entry['data_fields']['content']):
                    continue
                self.raw_entry = entry
                self.f_count = entry['data_fields']['file_count']
                self.f_size = entry['data_fields']['file_size']
            if self.raw_entry is None:
                raise Exception(f"No dicom entry found for series {series_num}")

    def get_format(self):
        for child in self.full_entry["children"]:
            for item in child["items"]:
                if 'data_fields' not in item:
                    continue
                if 'label' in item['data_fields']:
                    return item['data_fields']['label']
                else:
                    if 'format' in item['data_fields']:
                        return item['data_fields']['format']
        return 'DICOM'

    def __repr__(self):
        return f"<ScanFolder: {self.series}>"


def get_resources(exp):
    if not exp.resource_files:
        return {}
    return {
        ResourceFolder(entry).label: ResourceFolder(entry)
        for entry in exp.resource_files[0]
    }


def get_scans(exp):
    return {
        scan.series: ScanFolder(scan.series, scan.raw_json)
        for scan in exp.scans
    }


def get_digests(files):
    return {item['URI']: item['digest'] for item in files}


def check_resources(dm_exp, kcni_exp):
    dm_resources = get_resources(dm_exp)
    kcni_resources = get_resources(kcni_exp)

    diffs = {
        'missing': {},
        'differ': []
    }

    for folder in dm_resources:
        if folder == 'NOLABEL':
            # Ignore NOLABEL folders, they're a product of an old xnat_upload bug
            continue

        if dm_resources[folder].f_count == 0:
            # Ignore empty folders on our server
            continue

        if folder not in kcni_resources:
            r_id = dm_exp.resource_IDs[folder]
            file_list = dm_xnat.get_resource_list(
                dm_exp.project,
                dm_exp.subject,
                dm_exp.name,
                r_id
            )
            diffs['missing'][r_id] = file_list
        else:
            dm_rid = dm_exp.resource_IDs[folder]
            kcni_rid = kcni_exp.resource_IDs[folder]

            dm_files = dm_xnat.get_resource_list(
                dm_exp.project,
                dm_exp.subject,
                dm_exp.name,
                dm_rid
            )

            kcni_files = kcni_xnat.get_resource_list(
                kcni_exp.project,
                kcni_exp.subject,
                kcni_exp.name,
                kcni_rid
            )

            kcni_digests = get_digests(kcni_files)
            dm_digests = get_digests(dm_files)

            for uri in dm_digests:
                if uri not in kcni_digests:
                    diffs['missing'].setdefault(dm_rid, []).append(uri)
                elif dm_digests[uri] != kcni_digests[uri]:
                    diffs['differ'].append((dm_rid, uri))
    return diffs


def check_scans(dm_exp, kcni_exp):
    dm_scans = get_scans(dm_exp)
    kcni_scans = get_scans(kcni_exp)

    diffs = {
        'missing': [],
        'differ': {}
    }

    for series in dm_scans:
        if series not in kcni_scans:
            diffs['missing'].append((series, dm_scans[series].get_format()))
        elif dm_scans[series].f_count != kcni_scans[series].f_count:
            diffs[series] = {
                'dm_count': dm_scans[series].f_count,
                'kcni_count': kcni_scans[series].f_count,
                'format': dm_scans[series].get_format()
            }

    return diffs


def upload_scans(dm_exp, kcni_exp, missing):
    for series_num, series_type in missing:
        try:
            dicom_zip = dm_xnat.get_dicom(
                dm_exp.project, dm_exp.subject, dm_exp.name, series_num,
                file_type=series_type
            )
        except Exception as e:
            print(f"Failed downloading series {series_num} for {dm_exp.name}."
                  f" Reason - {e}")
            return

        try:
            kcni_xnat.put_dicoms(
                kcni_exp.project, kcni_exp.subject, kcni_exp.name, dicom_zip
            )
        except Exception as e:
            print(f"Failed uploading series {series_num} for {kcni_exp.name}."
                  f" Reason - {e}")

        try:
            os.remove(dicom_zip)
        except:
            pass


def upload_resources(dm_exp, kcni_exp, missing):
    for r_id in missing:
        for entry in missing[r_id]:
            try:
                source = dm_xnat.get_resource(
                    dm_exp.project, dm_exp.subject, dm_exp.name, r_id,
                    entry['URI'], zipped=False
                )
            except Exception as e:
                print(f"Failed uploading resource {entry['URI']} for "
                      f"{dm_exp.name}. Reason - {e}"
                )
                continue

            folder_name = os.path.dirname(entry['ID'])
            unquoted = urllib.parse.unquote(entry['URI'])

            if unquoted != entry['URI']:
                print(f"File name changed from {entry['URI']} to {unquoted}")

            with open(source, 'rb') as fh:
                try:
                    kcni_xnat.put_resource(
                        kcni_exp.project, kcni_exp.subject, kcni_exp.name,
                        unquoted, fh, folder_name
                    )
                except Exception as e:
                    print(f"Failed uploading {entry['URI']} for {dm_exp.name}."
                          f" Reason - {e}")
            try:
                os.remove(source)
            except:
                pass


def main():
    arguments = docopt(__doc__)
    study = arguments['<study>']
    dm_project = arguments['<dm_project>']
    kcni_project = arguments['<kcni_project>']
    dm_exp = arguments['<datman_exp>']
    output = arguments['--output']
    fix = arguments['--fix']
    site = arguments['--site']

    config = datman.config.config(study=study)
    try:
        id_map = config.get_key('ID_MAP')
    except:
        id_map = None

    if dm_exp:
        experiments = [dm_exp]
    else:
        experiments = dm_xnat.get_experiment_ids(dm_project)

    diffs = {}

    if not experiments:
        print(f"No experiments found on original server for {dm_project}. Check project name.")
        return

    for exp_id in experiments:
        try:
            dm_ident = datman.scanid.parse(exp_id)
        except datman.scanid.ParseException:
            print(f"Failed to parse experiment ID {exp_id}. Ignoring.")
            continue

        if site and site != dm_ident.site:
            continue

        try:
            kcni_ident = datman.scanid.get_kcni_identifier(exp_id, id_map)
        except datman.scanid.ParseException:
            print(f"Failed to parse ID {exp_id} into KCNI ID. Ignoring.")
            continue

        try:
            dm_exp = dm_xnat.get_experiment(
                dm_project,
                dm_ident.get_xnat_subject_id(),
                dm_ident.get_xnat_experiment_id()
            )
        except Exception:
            print(f"Couldnt find datman xnat experiment {exp_id}")
            continue

        try:
            kcni_exp = kcni_xnat.get_experiment(
                kcni_project,
                kcni_ident.get_xnat_subject_id(),
                kcni_ident.get_xnat_experiment_id()
            )
        except Exception:
            print(f"Couldnt find kcni xnat experiment for {kcni_ident.orig_id}")
            continue

        scan_diffs = check_scans(dm_exp, kcni_exp)
        res_diffs = check_resources(dm_exp, kcni_exp)

        diffs[exp_id] = {
            'missing_scans': scan_diffs['missing'],
            'missing_resources': res_diffs['missing']
        }

        if scan_diffs['differ'] or res_diffs['differ']:
            diffs[exp_id] = {
                'diff_scans': scan_diffs['differ'],
                'diff_resources': res_diffs['differ']
            }

        if fix:
            upload_scans(dm_exp, kcni_exp, scan_diffs['missing'])
            upload_resources(dm_exp, kcni_exp, res_diffs['missing'])

    if not output:
        print(f"Discovered differences: {diffs}")
        return

    if not diffs:
        return

    with open(output, 'w') as fh:
        yaml.dump(diffs, fh)


if __name__ == "__main__":
    main()
