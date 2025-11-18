import torch
from tqdm import trange, tqdm

@torch.no_grad()
def sample_rk4(model, x, steps=None, sigma_max=1, sigmas=None, callback=None, dist_shift=None, **extra_args):
    assert steps is not None or sigmas is not None, 'Either steps or sigmas must be provided'
    ts = x.new_ones([x.shape[0]])
    if sigmas is None:
        t = torch.linspace(sigma_max, 0, steps + 1)
        if dist_shift is not None:
            t = dist_shift.time_shift(t, x.shape[-1])
    else:
        t = sigmas
    for i, (t_curr, t_prev) in enumerate(tqdm(zip(t[:-1], t[1:]))):
        t_curr_tensor = t_curr * ts
        dt = t_prev - t_curr
        k1 = model(x, t_curr_tensor, **extra_args)
        k2 = model(x + dt / 2 * k1, (t_curr + dt / 2) * ts, **extra_args)
        k3 = model(x + dt / 2 * k2, (t_curr + dt / 2) * ts, **extra_args)
        k4 = model(x + dt * k3, t_prev * ts, **extra_args)
        x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if callback is not None:
            denoised = x - t_prev * k4
            callback({'x': x, 't': t_curr, 'sigma': t_curr, 'i': i + 1, 'denoised': denoised})
    return x