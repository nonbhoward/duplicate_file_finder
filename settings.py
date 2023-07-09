# Project settings

# imports, python
from os import environ
from os.path import exists
from pathlib import Path

home_drive = environ.get("HOMEDRIVE")
if not home_drive:
    raise OSError(f'Could not locate home_drive : {home_drive}')

# VARIABLES AND EXPLANATION
#   BUF_SIZE: for hash generation, limits RAM usage when hashing large files
#   home_drive: the primary hard drive, probably C:\
#   debug: set to True to enable developer mode, no files will be moved in
#       this mode, only copied
#   extensions: a list of the file extensions we are looking for
#   file_source: a list of elements that will be combined to
#       build the source search directory
#   file_destination: a list of elements that will be combined to
#       build the destination directory
settings = {
    'BUF_SIZE': 65536,
    'debug': True,
    'extensions': [
        #'mp4',
    ],
    'file_source': [
        #f'{home_drive}',
        'D:\\'
        'mega',
    ],
    'file_destination': [
        f'{home_drive}',
        'path_to_testing_destination',
    ]
}

# Verify required folders exist
file_source_elements = settings['file_source']
file_destination_elements = settings['file_destination']
path_to_source = str(Path('\\'.join(file_source_elements)))
path_to_destination = str(Path('\\'.join(file_destination_elements)))
if not exists(path_to_source):
    print(f'Path does not exist : {path_to_source}')
if not exists(path_to_destination):
    print(f'Path does not exist : {path_to_destination}')
