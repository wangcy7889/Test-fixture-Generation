import numpy as np

def vector_to_angle(vector: np.ndarray) -> np.ndarray:
    assert vector.shape == (3,)
    x, y, z = vector
    pitch = np.arcsin(-y)
    yaw = np.arctan2(-x, -z)
    return np.array([pitch, yaw])