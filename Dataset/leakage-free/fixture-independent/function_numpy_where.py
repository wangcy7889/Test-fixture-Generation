import numpy as np


def f_where(input_array, condition):
    return np.where(condition, input_array, 0)