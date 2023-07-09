# Project settings

# imports, python
from os import environ

home_drive = environ.get("HOMEDRIVE")
if not home_drive:
    raise OSError(f'Could not locate home_drive : {home_drive}')

# VARIABLES AND EXPLANATION
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
        'iso',
    ],
    'file_source': [
        f'{home_drive}',
        'path_to_testing_source',
    ],
    'file_destination': [
        f'{home_drive}',
        'path_to_testing_destination',
    ]
}
