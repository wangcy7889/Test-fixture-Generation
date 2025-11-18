import numpy as np

def segment2box(segment, width=640, height=640):
    x, y = segment.T
    x = x.clip(0, width)
    y = y.clip(0, height)
    return np.array([x.min(), y.min(), x.max(), y.max()], dtype=segment.dtype) if any(x) else np.zeros(4, dtype=segment.dtype)