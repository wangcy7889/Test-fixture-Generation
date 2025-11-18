import torch
from tqdm import trange

@torch.no_grad()
def sample_flow_pingpong(model, x, steps=None, sigma_max=1, sigmas=None, callback=None, dist_shift=None, **extra_args):
    assert steps is not None or sigmas is not None, 'Either steps or sigmas must be provided'
    ts = x.new_ones([x.shape[0]])
    if sigmas is None:
        t = torch.linspace(sigma_max, 0, steps + 1)
        if dist_shift is not None:
            t = dist_shift.time_shift(t, x.shape[-1])
    else:
        t = sigmas
    for i in trange(len(t) - 1, disable=False):
        denoised = x - t[i] * model(x, t[i] * ts, **extra_args)
        if callback is not None:
            callback({'x': x, 'i': i, 't': t[i], 'sigma': t[i], 'sigma_hat': t[i], 'denoised': denoised})
        t_next = t[i + 1]
        x = (1 - t_next) * denoised + t_next * torch.randn_like(x)
    return x