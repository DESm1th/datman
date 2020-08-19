#!/bin/bash
"""Report files missing from KCNI server.

Usage:
    find_missing.py [options] <dm_project> <kcni_project>
    find_missing.py [options] <dm_project> <kcni_project> <datman_exp>

Args:
    <dm_project>        The name of the project on our xnat server
    <kcni_project>      The name of the project on KCNI's server
    <datman_exp>        The datman ID of a specific experiment to check
"""
import os

from docopt import docopt

import datman.xnat

xnat_user = os.getenv("XNAT_USER")
xnat_pass = os.getenv("XNAT_PASS")

dm_server = "https://xnat.imaging-genetics.camh.ca"
kcni_server = "https://xnat.camh.ca/xnat"

dm_xnat = datman.xnat.xnat(dm_server, xnat_user, xnat_pass)
# kcni_xnat = datman.xnat.xnat(kcni_server, xnat_user, xnat_pass)


class ResourceFolder:

    def __init__(self, xnat_entry):
        self.entry = xnat_entry
        try:
            self.label = xnat_entry['data_fields']['label']
        except KeyError:
            self.label = 'NOLABEL'
        self.f_size = xnat_entry['data_fields']['file_size']
        self.f_count = xnat_entry['data_fields']['file_count']

    def __repr__(self):
        return f"<ResourceFolder: {self.label}>"


class ScanFolder:

    def __init__(self, series_num, xnat_entry):
        self.full_entry = xnat_entry
        self.series = series_num
        for child in xnat_entry['children']:
            if child['field'] != 'file':
                continue
            self.raw_entry = None
            for entry in child['items']:
                if 'SNAPSHOT' in entry['data_fields']['content']:
                    continue
                self.raw_entry = entry
                self.f_count = entry['data_fields']['file_count']
                self.f_size = entry['data_fields']['file_size']
            if self.raw_entry is None:
                raise Exception(f"No dicom entry found for series {series_num}")

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


def find_missing(dm_exp, kcni_exp):
    resource_diffs = check_resources(dm_exp, kcni_exp)


def check_resources(dm_exp, kcni_exp):
    dm_resources = get_resources(dm_exp)
    kcni_resources = get_resources(kcni_exp)

    diffs = {
        'missing': {},
        'differ': []
    }

    for folder in dm_resources:
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
        elif dm_resources[folder].f_count != kcni_resources[folder].f_count:
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
            kcni_uris = [entry['URI'] for entry in kcni_files]

            diffs['missing'][dm_rid] = []
            for entry in dm_files:
                if entry['URI'] not in kcni_uris:
                    diffs['missing'][dm_rid].append(entry)

        elif dm_resources[folder].f_size != kcni_resources[folder].f_size:
            entry = {
                'folder': folder,
                'dm_size': dm_resources[folder].f_size,
                'kcni_size': kcni_resources[folder].f_size
            }
            diffs['differ'].append(entry)

    return diffs




    # Find files that are the wrong size

    # Download missing files
    # report wrong sized files

    # Upload missing files with correct names

    # If entire folder missing.. add all contents to list
    # if only single file missing.. add to list
    # if file is wrong size... ??

    # missing list, wrong size list
    # missing = list of full paths to each file (include parent folders)
    # wrong_size = list of full path + size for each server

    # Write into (<src_proj>, <src_id>, <src_exp>), (<dest_proj>, <dest_id>, <dest_exp>), <full_path> (??)
    # src_tuple, full_path (size), dest_tuple, full_path (size)

    # missing {'scans': missing_scans, 'resources': missing_res}

    missing = []
    for folder in dm_resources:
        # Check if file count is greater than 0. Some 'NO LABEL' empty folders
        # exist on our server and shouldnt be replicated.
        if dm_resources[folder].f_count != 0 and folder not in kcni_resources:
            missing.append(folder)

    dm_resources = dm_exp.get_resources(dm_xnat)
    kcni_resources = kcni_exp.get_resources(kcni_xnat)
    missing_resources = list(set(dm_resources) - set(kcni_resources))

    # if missing_resources:
        # Compare file sizes of dm_exp.resource_files[0][0]['data_fields']
        # if data_fields['file_count'] is equal check data_fields['file_size']
    missing = []
    for entry in dm_exp.resource_files[0]:
        data_fields = entry['data_fields']
        label = data_fields['label']
        f_size = data_fields['file_size']
        f_count = data_fields['file_count']


def check_scans(dm_exp, kcni_exp):
    dm_scans = get_scans(dm_exp)
    kcni_scans = get_scans(kcni_exp)

    diffs = {
        'missing': [],
        'differ': {}
    }

    for series in dm_scans:
        if series not in kcni_scans:
            diffs['missing'].append(series)
        elif (dm_scans[series].f_size != kcni_scans[series].f_size or
              dm_scans[series].f_count != kcni_scans[series].f_count):
            diffs[series] = {
                'dm_size': dm_scans[series].f_size,
                'kcni_size': kcni_scans[series].f_size,
                'dm_count': dm_scans[series].f_count,
                'kcni_count': kcni_scans[series].f_count
            }

    return diffs


def upload_scans(dm_exp, kcni_exp, missing):
    for series_num in missing:
        try:
            dicom_zip = dm_xnat.get_dicom(
                dm_exp.project, dm_exp.subject, dm_exp.name, series_num
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
                    entry['URI']
                )
            except Exception as e:
                print(f"Failed uploading resource {entry['URI']} for "
                      f"{dm_exp.name}. Reason - {e}"
                )
                continue

            with open(source, 'rb') as fh:
                try:
                    kcni_xnat.put_resource(
                        kcni_exp.project, kcni_exp.subject, kcni_exp.name,
                        entry['URI'], fh, 'MISC'
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

if __name__ == "__main__":
    main()
