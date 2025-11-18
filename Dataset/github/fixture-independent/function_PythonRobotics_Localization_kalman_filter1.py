import math
import numpy as np
DT = 0.1

def motion_model(x, u):
    F = np.array([[1.0, 0, 0, 0], [0, 1.0, 0, 0], [0, 0, 1.0, 0], [0, 0, 0, 0]])
    B = np.array([[DT * math.cos(x[2, 0]), 0], [DT * math.sin(x[2, 0]), 0], [0.0, DT], [1.0, 0.0]])
    x = F @ x + B @ u
    return x