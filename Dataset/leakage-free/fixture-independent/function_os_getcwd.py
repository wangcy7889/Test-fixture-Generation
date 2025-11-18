import os


def get_directory_info(path=None):
    if path is None:
        path = os.getcwd()
    is_file = os.path.isfile(path)
    is_accessible = os.access(path, os.F_OK)
    is_empty = False
    if os.path.isdir(path):
        is_empty = len(os.listdir(path)) == 0
    _, extension = os.path.splitext(path)
    abs_path = os.path.abspath(path)
    return is_file, is_accessible, is_empty, extension, abs_path


