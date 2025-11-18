from itertools import permutations
from collections import defaultdict


def get_permutations(data):
    if not isinstance(data, str):
        raise ValueError("Input data must be a string.")
    perms = [''.join(p) for p in permutations(data)]
    perm_dict = defaultdict(int)
    for perm in perms:
        perm_dict[perm] += 1
    return perms, perm_dict