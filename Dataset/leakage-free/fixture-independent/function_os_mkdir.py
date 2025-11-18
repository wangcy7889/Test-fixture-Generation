import os


def f_mkdir(directory_path):
    try:
        os.mkdir(directory_path)
        return True
    except FileExistsError:
        return False
