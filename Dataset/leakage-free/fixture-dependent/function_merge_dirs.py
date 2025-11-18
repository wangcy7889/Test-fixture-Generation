import os
import shutil


def merge_folders(source_folder1, source_folder2, destination_folder):
    def copy_contents(source, destination):
        if not os.path.exists(source):
            raise FileNotFoundError(f"Error: Source path does not exist: {source}")
        for item in os.listdir(source):
            s = os.path.join(source, item)
            d = os.path.join(destination, item)
            try:
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            except Exception as e:
                raise Exception(e)
        return True

    if not os.path.exists(destination_folder):
        try:
            os.makedirs(destination_folder)
        except Exception as e:
            raise Exception(e)

    if not copy_contents(source_folder1, destination_folder):
        return False
    if not copy_contents(source_folder2, destination_folder):
        return False
    return True

