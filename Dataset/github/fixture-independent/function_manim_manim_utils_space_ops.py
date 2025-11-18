from __future__ import annotations
from collections.abc import Sequence
import numpy as np

def quaternion_mult(*quats: Sequence[float]) -> np.ndarray | list[float | np.ndarray]:
    if len(quats) == 0:
        return [1, 0, 0, 0]
    result = quats[0]
    for next_quat in quats[1:]:
        w1, x1, y1, z1 = result
        w2, x2, y2, z2 = next_quat
        result = [w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2, w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2, w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2, w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2]
    return result