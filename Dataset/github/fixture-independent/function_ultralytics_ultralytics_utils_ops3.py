import torch

def clip_coords(coords, shape):
    if isinstance(coords, torch.Tensor):
        coords[..., 0] = coords[..., 0].clamp(0, shape[1])
        coords[..., 1] = coords[..., 1].clamp(0, shape[0])
    else:
        coords[..., 0] = coords[..., 0].clip(0, shape[1])
        coords[..., 1] = coords[..., 1].clip(0, shape[0])
    return coords