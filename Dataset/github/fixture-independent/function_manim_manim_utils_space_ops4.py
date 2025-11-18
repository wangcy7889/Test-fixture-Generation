from __future__ import annotations
from collections.abc import Sequence
import numpy as np

def angle_of_vector(vector: Sequence[float] | np.ndarray) -> float:
    if isinstance(vector, np.ndarray) and len(vector.shape) > 1:
        if vector.shape[0] < 2:
            raise ValueError('Vector must have the correct dimensions. (2, n)')
        c_vec = np.empty(vector.shape[1], dtype=np.complex128)
        c_vec.real = vector[0]
        c_vec.imag = vector[1]
        val1: float = np.angle(c_vec)
        return val1
    val: float = np.angle(complex(*vector[:2]))
    return val