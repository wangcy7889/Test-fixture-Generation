from __future__ import annotations
from collections.abc import Sequence
import numpy as np

def cartesian_to_spherical(vec: Sequence[float]) -> np.ndarray:
    norm = np.linalg.norm(vec)
    if norm == 0:
        return (0, 0, 0)
    r = norm
    phi = np.arccos(vec[2] / r)
    theta = np.arctan2(vec[1], vec[0])
    return np.array([r, theta, phi])