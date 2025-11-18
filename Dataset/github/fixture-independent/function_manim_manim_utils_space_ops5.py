from __future__ import annotations
import numpy as np

def normalize(vect: np.ndarray | tuple[float], fall_back: np.ndarray | None=None) -> np.ndarray:
    norm = np.linalg.norm(vect)
    if norm > 0:
        return np.array(vect) / norm
    else:
        return fall_back or np.zeros(len(vect))