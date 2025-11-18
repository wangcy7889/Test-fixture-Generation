import torch
from tqdm import trange

@torch.no_grad()
def sample_flow_dpmpp(model, x, steps=None, sigma_max=1, sigmas=None, callback=None, dist_shift=None, disable_tqdm=False, **extra_args):
    assert steps is not None or sigmas is not None, 'Either steps or sigmas must be provided'
    ts = x.new_ones([x.shape[0]])
    if sigmas is None:
        t = torch.linspace(sigma_max, 0, steps + 1)
        if dist_shift is not None:
            t = dist_shift.time_shift(t, x.shape[-1])
    else:
        t = sigmas
    old_denoised = None
    log_snr = lambda t: ((1 - t) / t).log()
    for i in trange(len(t) - 1, disable=disable_tqdm):
        t_curr, t_next = (t[i], t[i + 1])
        denoised = x - t_curr * model(x, t_curr * ts, **extra_args)
        if callback is not None:
            callback({'x': x, 'i': i, 't': t_curr, 'sigma': t_curr, 'denoised': denoised})
        alpha_t = 1 - t_next
        h = log_snr(t_next) - log_snr(t_curr)
        if old_denoised is None or t_next == 0:
            x = t_next / t_curr * x - alpha_t * (-h).expm1() * denoised
        else:
            h_last = log_snr(t_curr) - log_snr(t[i - 1])
            r = h_last / h
            denoised_d = (1 + 1 / (2 * r)) * denoised - 1 / (2 * r) * old_denoised
            x = t_next / t_curr * x - alpha_t * (-h).expm1() * denoised_d
        old_denoised = denoised
    return x