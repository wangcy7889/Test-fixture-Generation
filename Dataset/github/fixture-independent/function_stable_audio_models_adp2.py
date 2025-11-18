import math
import torch

def get_extra_padding_for_conv1d(x: torch.Tensor, kernel_size: int, stride: int, padding_total: int=0) -> int:
    length = x.shape[-1]
    n_frames = (length - kernel_size + padding_total) / stride + 1
    ideal_length = (math.ceil(n_frames) - 1) * stride + (kernel_size - padding_total)
    return ideal_length - length