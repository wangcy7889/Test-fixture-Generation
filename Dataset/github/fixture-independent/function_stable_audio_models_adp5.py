import torch
from einops import rearrange, repeat
from torch import Tensor

def add_mask(sim: Tensor, mask: Tensor) -> Tensor:
    b, ndim = (sim.shape[0], mask.ndim)
    if ndim == 3:
        mask = rearrange(mask, 'b n m -> b 1 n m')
    if ndim == 2:
        mask = repeat(mask, 'n m -> b 1 n m', b=b)
    max_neg_value = -torch.finfo(sim.dtype).max
    sim = sim.masked_fill(~mask, max_neg_value)
    return sim