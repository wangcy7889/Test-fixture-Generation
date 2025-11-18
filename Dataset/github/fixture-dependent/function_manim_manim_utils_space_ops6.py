from __future__ import annotations
import numpy as np

def normalize_along_axis(array: np.ndarray, axis: np.ndarray) -> np.ndarray:
    norms = np.sqrt((array * array).sum(axis))
    norms[norms == 0] = 1
    buffed_norms = np.repeat(norms, array.shape[axis]).reshape(array.shape)
    array /= buffed_norms
    return array