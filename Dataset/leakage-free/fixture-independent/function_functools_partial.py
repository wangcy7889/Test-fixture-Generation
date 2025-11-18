from collections import defaultdict
from functools import partial


# 原始函数，计算两个数的和
def add_numbers(a, b):
    return a + b


# 使用partial创建一个新的函数，固定了add_numbers的第一个参数为5
add_five = partial(add_numbers, 5)


# 一个使用defaultdict的函数示例
def count_characters(string):
    char_count = defaultdict(int)
    for char in string:
        char_count[char] += 1
    return dict(char_count)