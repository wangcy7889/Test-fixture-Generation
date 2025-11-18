import itertools

# 示例函数，使用repeat函数创建一个迭代器并取前n个元素作为列表
def f_repeat(n, element):
    return list(itertools.islice(itertools.repeat(element), n))