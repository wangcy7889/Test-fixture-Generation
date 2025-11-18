import torch

def sample_flow_dpmpp_w_intermediates(model, x, sigmas=None, steps=None, callback=None, dist_shift=None, **extra_args):
    assert steps is not None or sigmas is not None, 'Either steps or sigmas must be provided'
    ts = x.new_ones([x.shape[0]])
    if sigmas is None:
        t = torch.linspace(1, 0, steps + 1)
        if dist_shift is not None:
            t = dist_shift.time_shift(t, x.shape[-1])
    else:
        t = sigmas
    old_denoised = None
    log_snr = lambda t: ((1 - t) / t).log()
    inters_x = []
    inters_t = []
    for i in range(len(t) - 1):
        inters_x.append(x)
        inters_t.append(t[i])
        denoised = x - t[i] * model(x, t[i] * ts, **extra_args)
        if callback is not None:
            callback({'x': x, 'i': i, 'sigma': t[i], 'sigma_hat': t[i], 'denoised': denoised})
        t_curr, t_next = (t[i], t[i + 1])
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
    target = x.detach()
    inters_x = torch.stack(inters_x).detach()
    inters_t = torch.stack(inters_t).unsqueeze(-1).detach()
    return {'target': target, 'x': inters_x, 't': inters_t}