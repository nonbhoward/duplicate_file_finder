# General use functions

# imports, python
from hashlib import md5
from os import stat
from os.path import exists


# Top-level functions
def this_is_a_file_we_care_about(path_to_file: str, settings: dict) -> bool:
    extensions = settings['extensions']
    if not extensions:
        return True  # No extensions listed, care about all files
    path_to_destination = build_path_using_(settings['file_destination'])
    path_to_file_parent_dir = build_path_using_(path_to_file.split('\\')[:-1])
    if path_to_destination == path_to_file_parent_dir:
        return False  # We don't care about files in the destination
    file_ext = get_extension(path_to_file)
    if not file_ext:
        return False  # We don't care about files without extensions
    if file_ext not in extensions:
        return False  # We don't care about extensions not listed in our search
    print(f'\tFound a matching file : {path_to_file}')
    return True


# Child functions
def append_guid_to_(filename, index) -> str:
    filename_elements = filename.split('\\')
    fn_w_guid = filename_elements[-1].split('.')
    filename_with_guid = fn_w_guid[0] + str(index) + '.' + fn_w_guid[-1]
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
    print(f'\tGenerating hash for : {file}')
    with open(file, 'rb') as f_rb:
        while True:
            f_data = f_rb.read(BUF_SIZE)
            if not f_data:
                break
            f_md5.update(f_data)
    f_hash = f_md5.hexdigest()
    return f_hash


def get_extension(path_to_file: str) -> str:
    extension = None
    filename = path_to_file.split('\\')[-1]
    if filename and '.' in filename:
        extension = filename.split('.')[-1]
    return extension


def identify_duplicate_files(found_files_with_metadata_sorted, settings):
    print('Identifying duplicate files')
    # Look for multiple entries with the same size
    unique_file_hashes = {}
    unique_files_and_duplicate_files = {
        'unique_files': {},
        'duplicate_files': {}
    }
    for file, file_details in found_files_with_metadata_sorted.items():
        file_hash = generate_hash_for_(file, settings)
        if file_hash not in unique_file_hashes:
            unique_file_hashes.update({file_hash: file})
            unique_files_and_duplicate_files['unique_files'].update({
                file_hash: {
                    'path_to_file': file,
                    'file_hash': file_hash
                }
            })
            continue  # Unique file found

        # Duplicate file found, process it and store its parent
        file_name = file.split('\\')[-1].split('.')[0]
        print(f'\tDuplicate file hash found for file : {file_name}')
        unique_files_and_duplicate_files['duplicate_files'].update({
            file: {
                'path_to_parent_duplicate':
                    unique_file_hashes[file_hash]
            }
        })
    return unique_files_and_duplicate_files


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
