import torch

def sample_timesteps_logsnr(batch_size, mean_logsnr=-1.2, std_logsnr=2.0):
    logsnr = torch.randn(batch_size) * std_logsnr + mean_logsnr
    t = torch.sigmoid(-logsnr)
    t = t.clamp(0.0001, 1 - 0.0001)
    return t