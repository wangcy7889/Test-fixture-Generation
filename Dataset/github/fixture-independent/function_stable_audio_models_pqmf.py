import numpy as np
import torch

def generate_modulated_filter_bank(prototype_filter, num_bands):
    subband_indices = torch.arange(num_bands).reshape(-1, 1)
    filter_length = prototype_filter.shape[-1]
    time_indices = torch.arange(-(filter_length // 2), filter_length // 2 + 1)
    phase_offsets = (-1) ** subband_indices * np.pi / 4
    modulation = torch.cos((2 * subband_indices + 1) * np.pi / (2 * num_bands) * time_indices + phase_offsets)
    modulated_filters = 2 * prototype_filter * modulation
    return modulated_filters