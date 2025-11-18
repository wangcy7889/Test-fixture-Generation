import torch

def get_dbmax(audio):
    return 20 * torch.log10(torch.flatten(audio.abs()).max()).cpu().numpy()