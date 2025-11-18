import torch

def checkpoint(function, *args, **kwargs):
    kwargs.setdefault('use_reentrant', False)
    return torch.utils.checkpoint.checkpoint(function, *args, **kwargs)