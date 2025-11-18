import sys


def sys_modules(module_data=None):
    if module_data is None:
        module_data = sys.modules
    result = []
    for module_name, module in module_data.items():
        result.append((module_name, module))
    return result