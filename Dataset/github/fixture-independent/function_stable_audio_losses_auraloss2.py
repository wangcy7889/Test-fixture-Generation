import torch
import scipy.signal

def get_window(win_type: str, win_length: int):
    try:
        win = getattr(torch, win_type)(win_length)
    except:
        win = torch.from_numpy(scipy.signal.windows.get_window(win_type, win_length))
    return win