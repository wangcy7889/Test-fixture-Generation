from __future__ import annotations
import numpy as np

def rotation_about_z(angle: float) -> np.ndarray:
    c, s = (np.cos(angle), np.sin(angle))
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])