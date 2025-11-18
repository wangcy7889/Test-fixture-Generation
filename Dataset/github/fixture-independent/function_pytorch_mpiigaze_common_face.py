import numpy as np

def change_coordinate_system(euler_angles: np.ndarray) -> np.ndarray:
    return euler_angles * np.array([-1, 1, -1])