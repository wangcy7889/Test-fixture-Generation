from __future__ import annotations
from typing import Callable
import numpy as np

def binary_search(function: Callable[[float], float], target: float, lower_bound: float, upper_bound: float, tolerance: float=0.0001) -> float | None:
    lh = lower_bound
    rh = upper_bound
    mh: float = np.mean(np.array([lh, rh]))
    while abs(rh - lh) > tolerance:
        mh = np.mean(np.array([lh, rh]))
        lx, mx, rx = (function(h) for h in (lh, mh, rh))
        if lx == target:
            return lh
        if rx == target:
            return rh
        if lx <= target <= rx:
            if mx > target:
                rh = mh
            else:
                lh = mh
        elif lx > target > rx:
            lh, rh = (rh, lh)
        else:
            return None
    return mh