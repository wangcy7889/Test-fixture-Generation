import numpy as np
from numpy.typing import NDArray
from typing import Optional

def sharpe_ratio(changes: NDArray[np.float64], obs: Optional[int]=None, downside_only: bool=False) -> np.floating:
    std_changes = changes[changes < 0] if downside_only else changes
    if not len(std_changes):
        return np.float64(0)
    std = np.std(std_changes)
    if std == 0:
        return np.float64(0)
    sr = np.mean(changes) / std
    if obs is not None:
        sr *= np.sqrt(obs)
    return sr