# imports, project
from mainlib import *
from settings import settings

# Find files
found_files = find_files_with_extension_(settings)

# Filter duplicates
filtered_files = filter_files(found_files, settings)

# Move/copy files, files will only be copied if debug is set to True in
#   settings
move_files_to_destination(filtered_files, settings)
