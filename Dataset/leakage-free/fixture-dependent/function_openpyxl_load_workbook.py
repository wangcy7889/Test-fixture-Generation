import openpyxl

def openpyxl_load_workbook(file_path, read_only=False, data_only=False):
    try:
        workbook = openpyxl.load_workbook(file_path, read_only=read_only, data_only=data_only)
        return workbook
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file was not found.")
    except Exception as e:
        raise RuntimeError(f"Error: An error occurred while loading the workbook: {e}")
