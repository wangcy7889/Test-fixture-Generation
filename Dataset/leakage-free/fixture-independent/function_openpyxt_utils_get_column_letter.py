from openpyxl.utils import get_column_letter

def convert_nested_column_numbers_to_letters(column_numbers_list):
    def convert_list(lst):
        return [convert_list(x) if isinstance(x, list) else get_column_letter(x) for x in lst]

    return convert_list(column_numbers_list)
