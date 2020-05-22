"""Update the dashboard's configuration based on the config yaml files.

This script should be run by a user with permission to update the dashboard's
database.

Any new studies that are found will be added, old values are updated
to match the config files wherever the database differs. The user is also given
the option to delete any records (tags, studies, sites) that aren't found in
the config files. Be warned: these deletes will cascade to scans that reference
the bad values (e.g. deleting a tag that's no longer used for a study like
'FMAP' will also delete all scan records for that study with that tag).

Usage:
    update_config.py [options]
    update_config.py [options] <study>

Args:
    <study>         Only update the configuration for the given study. Note
                    that this will cause errors if a tag is entirely new
                    (i.e. the global configuration must define a tag before
                    a study can reference it).

Options:
    --delete        Delete tags, studies and sites not found in config files
                    without prompting the user. This will cascade to records
                    that reference the outdated configuration.
    --skip          Skip all user prompts (delete nothing).
    --quiet, -q     Only report errors.
    --verbose, -v   Be chatty.
    --debug, -d     Be extra chatty.
"""
import os
import logging

from docopt import docopt

import datman.dashboard
import datman.config
from datman.exceptions import UndefinedSetting

logging.basicConfig(level=logging.WARN,
                    format="[%(name)s] %(levelname)s: %(message)s")
logger = logging.getLogger(os.path.basename(__file__))

DELETE = False
SKIP_DELETE = False


def main():
    global DELETE, SKIP_DELETE

    args = docopt(__doc__)
    study = args['<study>']
    DELETE = args['--delete']
    SKIP_DELETE = args['--skip']
    quiet = args['--quiet']
    verbose = args['--verbose']
    debug = args['--debug']

    if verbose:
        logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    if quiet:
        logger.setLevel(logging.ERROR)

    if not datman.dashboard.dash_found:
        logger.error('Dashboard not found or incorrectly configured. Exiting.')
        return

    config = datman.config.config()

    if study:
        update_study(study, config)
        return

    # Update tag list + scan types + pha types

    # offer to delete studies not found in projects list

    try:
        studies = config.get_key('Projects').keys()
    except UndefinedSetting:
        logger.info('No configured projects detected.')
        studies = []

    for study in studies:
        update_study(study, config)


def update_study(study_id, config):
    study = datman.dashboard.get_project(study_id, create=True)

    # if Description defined, update description
    # FullName, update name
    # if OPEN_STUDY, update is_open

    # readme -> requires finding and reading file
    # PrimaryContact (need to add user + fill in study_user record?)
    # Sites -> Add study_site record for each + add new sites
    #       (offer to delete study_site records that don't match + cascade to scan records)
    # Scan types -> add a scantype + study_scantype record as needed (delete study_scantype records)
    # USES_TECHNOTES (may be study wide or site in config files, add to study_site records)
    # STUDY_TAG -> may change by site, provide site when getting key
    #       (alt study codes?...)
    # Expected scans -> Add record for each tag + add counts
    #       (offer to delete study/site/tag combos no longer found + cascade)
    # email on trigger? Is there config val for that?
    # USES_REDCAP -> Update study_sites records

    return


def update_tags(config, skip_delete=False, delete_all=False):
    try:
        tag_settings = config.get_key('ExportSettings')
    except UndefinedSetting:
        logger.info('No defined tags found, skipping tag update.')
        return

    for tag in tag_settings:
        settings = tag_settings[tag]
        db_entry = datman.dashboard.get_tags(tag, create=True)[0]
        try:
            qc_type = settings['qc_type']
        except KeyError:
            qc_type = None
        try:
            pha_type = settings['qc_pha']
        except KeyError:
            pha_type = None
        db_entry.qc_type = qc_type
        db_entry.pha_type = pha_type
        db_entry.save()

    all_tags = datman.dashboard.get_tags()
    undefined = []
    for record in all_tags:
        if record.tag not in tag_settings:
            undefined.append(record)

    if undefined:
        delete_tags(undefined, skip_delete, delete_all)


def delete_tags(records, skip_delete=False, delete_all=False):
    logger.info(f"Found {len(records)} tags in database that are not "
                "defined in config files.")

    if skip_delete:
        return

    for record in records:
        tagged_scans = datman.dashboard.find_scans(record.tag)

        if delete_all:
            remove = True
        else:
            remove = prompt_user(
                f"{record} missing from config files. If deleted, "
                f"{len(tagged_scans)} scan records will also be removed. "
                "Delete? (y/[n]) ")

        if not remove:
            continue

        logger.info(f"Removing tag {record} and {len(tagged_scans)} scans.")

        try:
            record.delete()
        except Exception as e:
            logger.error(f"Failed deleting {record}. Reason - {e}")


def prompt_user(message):
    answer = input(message).lower()
    if answer not in ['y', 'n', '']:
        raise RuntimeError(f"Invalid user input {answer}")
    return answer == 'y'


if __name__ == "__main__":
    main()
