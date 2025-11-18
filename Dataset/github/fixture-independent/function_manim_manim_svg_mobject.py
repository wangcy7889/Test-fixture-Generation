from __future__ import annotations
import numpy as np

def _convert_point_to_3d(x: float, y: float) -> np.ndarray:
    return np.array([x, y, 0.0])