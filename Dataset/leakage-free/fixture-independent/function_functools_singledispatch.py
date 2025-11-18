from collections import defaultdict
from functools import singledispatch


# 通用的处理函数，对于未专门处理的类型会抛出异常
@singledispatch
def f_singledispatch(data):
    raise NotImplementedError(f"不支持的数据类型: {type(data)}")


# 处理整数类型，将其乘以2
@f_singledispatch.register(int)
def _(data):
    return data * 2


# 处理字符串类型，将其转换为大写
@f_singledispatch.register(str)
def _(data):
    return data.upper()


# 处理列表类型，返回列表长度
@f_singledispatch.register(list)
def _(data):
    return len(data)


# 处理defaultdict类型，返回其键值对数量
@f_singledispatch.register(defaultdict)
def _(data):
    return len(data)


# 处理元组类型，返回元组长度
@f_singledispatch.register(tuple)
def _(data):
    return len(data)

