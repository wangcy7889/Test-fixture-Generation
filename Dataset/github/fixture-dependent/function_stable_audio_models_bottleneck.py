import torch
from torch import nn

def vae_sample(mean, scale):
    stdev = nn.functional.softplus(scale) + 0.0001
    var = stdev * stdev
    logvar = torch.log(var)
    latents = torch.randn_like(mean) * stdev + mean
    kl = (mean * mean + var - logvar - 1).sum(1).mean()
    return (latents, kl)