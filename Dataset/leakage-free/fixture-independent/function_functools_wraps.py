from functools import wraps
from collections import defaultdict


def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Before calling {func.__name__}")
        # 使用defaultdict模拟一些额外的功能
        my_dict = defaultdict(int)
        my_dict[func.__name__] += 1
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred in {func.__name__}: {e}")
            raise
        print(f"After calling {func.__name__}")
        print(f"Function {func.__name__} has been called {my_dict[func.__name__]} times")
        return result
    return wrapper


@my_decorator
def add_numbers(a, b):
    return a + b


@my_decorator
def multiply_numbers(a, b):
    return a * b


@my_decorator
def divide_numbers(a, b):
    return a / b