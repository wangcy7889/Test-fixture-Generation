import numpy as np


def f_divide(arr1, arr2=None, scalar=None):
    if arr2 is not None:
        return np.divide(arr1, arr2)
    elif scalar is not None:
        return np.divide(arr1, scalar)