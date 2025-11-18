from typing import Any
import numpy as np

def find_pivot(self) -> tuple[Any, Any]:
    objective = self.objectives[-1]
    sign = (objective == 'min') - (objective == 'max')
    col_idx = np.argmax(sign * self.tableau[0, :-1])
    if sign * self.tableau[0, col_idx] <= 0:
        self.stop_iter = True
        return (0, 0)
    s = slice(self.n_stages, self.n_rows)
    dividend = self.tableau[s, -1]
    divisor = self.tableau[s, col_idx]
    nans = np.full(self.n_rows - self.n_stages, np.nan)
    quotients = np.divide(dividend, divisor, out=nans, where=divisor > 0)
    row_idx = np.nanargmin(quotients) + self.n_stages
    return (row_idx, col_idx)