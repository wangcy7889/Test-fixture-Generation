import numpy as np
import torch
AUDIO_KEYS = ('flac', 'wav', 'mp3', 'm4a', 'ogg', 'opus')

def collation_fn(samples):
    batched = list(zip(*samples))
    result = []
    for b in batched:
        if isinstance(b[0], (int, float)):
            b = np.array(b)
        elif isinstance(b[0], torch.Tensor):
            b = torch.stack(b)
        elif isinstance(b[0], np.ndarray):
            b = np.array(b)
        else:
            b = b
        result.append(b)
    return result