# General use functions

# imports, python
from hashlib import md5
from os import stat
from os.path import exists


# Top-level functions
def this_is_a_file_we_care_about(path_to_file: str, settings: dict) -> bool:
    extensions = settings['extensions']
    path_to_destination = build_path_using_(settings['file_destination'])
    path_to_file_parent_dir = build_path_using_(path_to_file.split('\\')[:-1])
    if path_to_destination == path_to_file_parent_dir:
        return False
    file_ext = get_extension(path_to_file)
    # Do not search in the path that is defined as a destination path
    if not file_ext:
        return False  # We don't care about files without extensions
    if file_ext not in extensions:
        return False  # We don't care about extensions not listed in our search
    return True


# Child functions
def append_guid_to_(filename, index) -> str:
    filename_elements = filename.split('\\')
    fn_w_guid = filename_elements[-1].split('.')
    filename_with_guid = fn_w_guid[0] + str(index) + '.' + fn_w_guid[1]
    return filename_with_guid


def build_path_using_(path_elements: list) -> str:
    if len(path_elements) < 2:
        return '\\'.join(path_elements) + '\\'
    return '\\'.join(path_elements)


def extract_metadata_from_(found_file: str) -> dict:
    """Available attributes :
        st_mode, st_ino, st_dev, st_nlink, st_uid, st_gid, st_size, st_atime,
        st_mtime, st_ctime
        https://docs.python.org/3/library/stat.html#module-stat """
    if not exists(found_file):
        print(f'No file found at : {found_file}')
    found_file_stat = stat(found_file)
    found_file_metadata = {
        'size': found_file_stat.st_size,
    }
    return found_file_metadata


def generate_hash_for_(file, settings):
    BUF_SIZE = settings['BUF_SIZE']
    f_md5 = md5()
    with open(file, 'rb') as f_rb:
        while True:
            f_data = f_rb.read(BUF_SIZE)
            if not f_data:
                break
            f_md5.update(f_data)
    f_hash = f_md5.hexdigest()
    return


def get_extension(path_to_file: str) -> str:
    extension = None
    filename = path_to_file.split('\\')[-1]
    if filename and '.' in filename:
        extension = filename.split('.')[-1]
    return extension


def identify_duplicate_files(found_files_with_metadata_sorted, settings):
    # Look for multiple entries with the same size
    unique_file_sizes = {}
    found_files_with_duplicates = {
        'unique_files': [],
        'duplicate_files': {}
    }
    for file, file_details in found_files_with_metadata_sorted.items():
        file_size = file_details['size']
        # Use the file size as a quick filter to identify unique files
        if file_size not in unique_file_sizes:
            unique_file_sizes.update({file_size: file})
            found_files_with_duplicates['unique_files'].append(file)
            continue
        file_name = file.split('\\')[-1].split('.')[0]

        # If the file sizes are the same, compare the file hashes
        # At this point, I know that this file size has been seen before
        # Generate a hash against the file contents

        # f_hash = generate_hash_for_(file, settings)

        print(f'Duplicate file size found for file : {file_name}')
        found_files_with_duplicates['duplicate_files'].update({
            file: {
                'path_to_parent_duplicate': unique_file_sizes[file_size]
            }
        })
    return found_files_with_duplicates


def populate_metadata_of_(found_files: list) -> dict:
    found_file_metadata = {}
    for found_file in found_files:
        file_metadata = extract_metadata_from_(found_file)
        if not file_metadata:
            continue
        found_file_metadata.update({
            found_file: file_metadata
        })
    return found_file_metadata
