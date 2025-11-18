import os

def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        return True
    except Exception as e:
        raise  Exception(f"An error occurred while renaming the file: {e}")