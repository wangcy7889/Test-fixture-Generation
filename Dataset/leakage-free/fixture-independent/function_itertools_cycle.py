import itertools


# 要测试的函数
def f_cycle(input_sequence, num_elements):
    cycle_iter = itertools.cycle(input_sequence)
    result = [next(cycle_iter) for _ in range(num_elements)]
    return result
