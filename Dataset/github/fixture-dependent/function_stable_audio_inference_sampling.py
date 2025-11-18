import torch
from tqdm import trange, tqdm

@torch.no_grad()
def sample_discrete_euler(model, x, steps=None, sigma_max=1, sigmas=None, callback=None, dist_shift=None, disable_tqdm=False, **extra_args):
    assert steps is not None or sigmas is not None, 'Either steps or sigmas must be provided'
    ts = x.new_ones([x.shape[0]])
    if sigmas is None:
        t = torch.linspace(sigma_max, 0, steps + 1)
        if dist_shift is not None:
            t = dist_shift.time_shift(t, x.shape[-1])
    else:
        t = sigmas
    for i, (t_curr, t_prev) in enumerate(tqdm(zip(t[:-1], t[1:]), disable=disable_tqdm)):
        t_curr_tensor = t_curr * torch.ones((x.shape[0],), dtype=x.dtype, device=x.device)
        dt = t_prev - t_curr
        v = model(x, t_curr_tensor, **extra_args)
        x = x + dt * v
        if callback is not None:
            denoised = x - t_prev * v
            callback({'x': x, 't': t_curr, 'sigma': t_curr, 'i': i + 1, 'denoised': denoised})
    return x