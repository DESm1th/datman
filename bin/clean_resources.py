#!/usr/bin/env python
"""Compare a newly downloaded set of files to a backed up copy to report
missing files.

Usage:
    clean_resources.py [options] <new_copy> <old_copy>

Args:
    <new_copy>      The full path to the newly downloaded copy of files.
    <old_copy>      The full path to the original copy.

Options:
    --output <path>     The full path to write any found differences to.

"""
import os
import glob
import hashlib

from docopt import docopt
import yaml

BUFFER_SIZE = 131072


def hash_file(file_path):
    sha = hashlib.sha3_512()
    with open(file_path, 'rb') as in_file:
        while True:
            data = in_file.read(BUFFER_SIZE)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


def compare_folder(old_copy, new_copy, folder):
    old_folder = os.path.join(old_copy, folder)
    new_folder = os.path.join(new_copy, folder)

    differ = []
    missing = []
    for path, _, files in os.walk(old_folder):
        for item in files:
            old_file = os.path.join(path, item)
            new_file = old_file.replace(old_folder, new_folder)
            if not os.path.exists(new_file):
                missing.append(new_file.replace(new_folder, ""))
            else:
                old_hash = hash_file(old_file)
                new_hash = hash_file(new_file)
                if old_hash != new_hash:
                    differ.append(new_file.replace(new_folder, ""))

    return {'differ': differ, 'missing': missing}


def main():
    args = docopt(__doc__)
    new_copy = args['<new_copy>']
    old_copy = args['<old_copy>']
    output = args['--output']

    old_folders = [os.path.basename(item) for item in glob.glob(old_copy + "/*")]
    new_folders = [os.path.basename(item) for item in glob.glob(new_copy + "/*")]

    missing = [item for item in old_folders if item not in new_folders]
    matched = [item for item in old_folders if item in new_folders]

    diffs = {'absent': missing}
    for subid in matched:
        diffs[subid] = compare_folder(old_copy, new_copy, subid)

    if not output:
        print(f"Discovered differences: {diffs}")
        return

    with open(output, 'w') as fh:
        yaml.dump(diffs, fh)


if __name__ == "__main__":
    main()
