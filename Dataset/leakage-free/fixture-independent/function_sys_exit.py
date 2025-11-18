import sys


def f_exit(num1, num2, operation_type, extra_param=None):
    if extra_param is not None and (isinstance(extra_param, str) or isinstance(extra_param, list)):
        print("Incorrect type of extra parameter. Program exiting.")
        sys.exit(12)
    if operation_type not in ['divide']:
        print("Unsupported operation type. Program exiting.")
        sys.exit(10)
    if num2 == 0:
        print("The divisor cannot be zero in division operation. Program exiting.")
        sys.exit(11)
    elif operation_type == 'divide':
        return num1 / num2