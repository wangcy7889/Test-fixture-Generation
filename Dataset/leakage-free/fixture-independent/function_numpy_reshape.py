import numpy as np


def f_reshape(input_array, new_shape):
    try:
        return np.reshape(input_array, new_shape)
    except ValueError as e:
        print(f"Error: {e}")
        return None