#!/usr/bin/env python
"""
Update series numbers for scans with malformed number fields.

Usage:
    anonymize_headers.py [options] <scan_folder>

Arguments:
    <scan_folder>      The full path to the scan folder of an extracted
                       zip file.

Options:
    -v, --verbose
    -d, --debug
"""
import os
import glob
import logging

import pydicom as dcm

from docopt import docopt

logging.basicConfig()
logger = logging.getLogger(os.path.basename(__file__))

def main():
    arguments = docopt(__doc__)
    verbose = arguments['--verbose']
    debug = arguments['--debug']

    if verbose:
        logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)

    in_dir = arguments['<scan_folder>']

    update_series(in_dir)

def update_series(input_dir):
    for series in glob.glob(input_dir + "*_MR1_*"):
        logger.info("Working on {}".format(series))

        new_num = os.path.basename(series).split("_")[0]
        for cur_dir, sub_dirs, files in os.walk(series):
            for item in files:
                dicom_path = os.path.join(cur_dir, item)
                try:
                    header = dcm.read_file(dicom_path)
                except dcm.filereader.InvalidDicomError:
                    continue

                header.SeriesNumber = new_num
                header.save_as(dicom_path)


if __name__ == '__main__':
    main()
