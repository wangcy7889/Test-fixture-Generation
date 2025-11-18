from __future__ import annotations
from collections.abc import Sequence
import numpy as np

def quaternion_conjugate(quaternion: Sequence[float]) -> np.ndarray:
    result = np.array(quaternion)
    result[1:] *= -1
    return result