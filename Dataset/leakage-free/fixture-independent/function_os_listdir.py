import os


def f_listdir(directory_path):
    try:
        return os.listdir(directory_path)
    except FileNotFoundError:
        return []