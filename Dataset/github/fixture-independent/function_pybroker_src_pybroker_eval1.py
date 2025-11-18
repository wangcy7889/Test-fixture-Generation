import numpy as np
from numpy.typing import NDArray

def profit_factor(changes: NDArray[np.float64], use_log: bool=False) -> np.floating:
    wins = changes[changes > 0]
    losses = changes[changes < 0]
    if not len(wins) and (not len(losses)):
        return np.float64(0)
    numer = denom = 1e-10
    numer += np.sum(wins)
    denom -= np.sum(losses)
    if use_log:
        return np.log(numer / denom)
    else:
        return np.divide(numer, denom)