import patoolib

def extract_archive(archive_file_path, output_dir_path, verbosity=0):

    import os
    if not isinstance(archive_file_path, str) or not isinstance(output_dir_path, str):
        raise ValueError("Error: archive_file_path and output_dir_path must be str.")
    if not os.path.isfile(archive_file_path):
        raise FileNotFoundError("Error: Archive file does not exist.")
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    try:
        patoolib.extract_archive(archive_file_path, outdir=output_dir_path, verbosity=verbosity)
        return True
    except Exception as e:
        raise Exception(f"Error: Extraction failed: {e}")

