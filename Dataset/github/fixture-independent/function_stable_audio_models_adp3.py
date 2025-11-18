import torch
import typing as tp

def unpad1d(x: torch.Tensor, paddings: tp.Tuple[int, int]):
    padding_left, padding_right = paddings
    assert padding_left >= 0 and padding_right >= 0, (padding_left, padding_right)
    assert padding_left + padding_right <= x.shape[-1]
    end = x.shape[-1] - padding_right
    return x[..., padding_left:end]