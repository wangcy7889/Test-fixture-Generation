from __future__ import annotations
from scipy import special

def choose(n: int, k: int) -> int:
    value: int = special.comb(n, k, exact=True)
    return value