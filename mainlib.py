# Functions directly called in main

# imports, python
from os import mkdir
from os import walk
from os.path import exists
from pathlib import Path
import shutil

# imports, project
from lib import append_guid_to_
from lib import build_path_using_
from lib import this_is_a_file_we_care_about
from lib import identify_duplicate_files
from lib import populate_metadata_of_


def filter_files(found_files: list, settings):
    # Populate metadata of each file
    found_files_with_metadata = ff_w_md = populate_metadata_of_(found_files)

    # Sort files by size
    ff_w_md_sorted = \
        {k: v for k, v in sorted(ff_w_md.items(),
                                 key=lambda item: item[1]['size'])}

    # Stage files for action
    # Identify duplicate files
    files_w_duplicates_identified = identify_duplicate_files(
        ff_w_md_sorted,
        settings)

    # What is the next step?
    return files_w_duplicates_identified


def find_files_with_extension_(settings: dict):
    # Declare initial vars
    files_we_care_about = []

    # Build path to settings
    file_src_path_elements = settings['file_source']
    file_src = build_path_using_(file_src_path_elements)

    # Read settings
    if not exists(file_src):
        raise OSError(f"Path does not exist : {file_src}")

    # Search root path, collecting desired files
    for root, _, files in walk(file_src):
        for file in files:
            path_to_file = str(Path(root, file))
            if this_is_a_file_we_care_about(path_to_file, settings):
                files_we_care_about.append(path_to_file)

    # Clean up and return
    return files_we_care_about


def move_files_to_destination(found_files: dict, settings: dict):
    debug = settings['debug']
    file_destination = build_path_using_(settings['file_destination'])
    # Move unique files to destination
    for file_hash, file_details in found_files['unique_files'].items():
        path_to_file = file_details['path_to_file']
        print(f'Move/Copy file :')
        print(f'\tFrom : {path_to_file}')
        print(f'\tTo : {file_destination}')
        try:
            if debug:
                shutil.copy(
                    src=path_to_file,
                    dst=file_destination
                )
                continue
            shutil.move(
                src=path_to_file,
                dst=file_destination
            )
        except Exception as exc:
            print(f'{exc}')
            print(f'Unable to copy/move file : {path_to_file}')

    # Move duplicate files to duplicate destination
    # Create the duplicate destination
    duplicate_destination = build_path_using_([file_destination, 'duplicates'])
    if not exists(duplicate_destination):
        try:
            mkdir(duplicate_destination)
        except Exception as exc:
            print(f'Failed to mkdir : {duplicate_destination}')
            raise exc

    # Move the duplicate files, appending a GUID to the filename to
    #   avoid overwrites
    for index, path_to_duplicate_file in enumerate(found_files['duplicate_files']):
        duplicate_filename_w_guid = append_guid_to_(path_to_duplicate_file, index)
        duplicate_destination_with_filename_appended = \
            str(Path(duplicate_destination, duplicate_filename_w_guid))
        print(f'Move/Copy file :')
        print(f'\tFrom : {path_to_duplicate_file}')
        print(f'\tTo : {file_destination}')
        try:
            if debug:
                shutil.copy(
                    src=path_to_duplicate_file,
                    dst=duplicate_destination_with_filename_appended
                )
                continue
            shutil.move(
                src=path_to_duplicate_file,
                dst=duplicate_destination_with_filename_appended
            )
        except Exception as exc:
            print(f'{exc}')
            print(f'Unable to copy/move file : {path_to_duplicate_file}')
