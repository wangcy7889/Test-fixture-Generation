from __future__ import annotations
from collections.abc import Sequence
import numpy as np

def spherical_to_cartesian(spherical: Sequence[float]) -> np.ndarray:
    r, theta, phi = spherical
    return np.array([r * np.cos(theta) * np.sin(phi), r * np.sin(theta) * np.sin(phi), r * np.cos(phi)])