import math
import torch as th

def compute_density_for_timestep_sampling(weighting_scheme: str, batch_size: int, logit_mean: float=None, logit_std: float=None, mode_scale: float=None):
    if weighting_scheme == 'logit_normal':
        u = th.normal(mean=logit_mean, std=logit_std, size=(batch_size,), device='cpu')
        u = th.nn.functional.sigmoid(u)
    elif weighting_scheme == 'mode':
        u = th.rand(size=(batch_size,), device='cpu')
        u = 1 - u - mode_scale * (th.cos(math.pi * u / 2) ** 2 - 1 + u)
    elif weighting_scheme == 'logit_normal_trigflow':
        sigma = th.randn(batch_size, device='cpu')
        sigma = (sigma * logit_std + logit_mean).exp()
        u = th.atan(sigma / 0.5)
    else:
        u = th.rand(size=(batch_size,), device='cpu')
    return u