import torch

def flat_pairwise_sq_distance(x, y):
    x_norm = (x ** 2).mean(dim=1, keepdim=True)
    y_norm = (y ** 2).mean(dim=1, keepdim=True).transpose(0, 1)
    return x_norm + y_norm - 2.0 * torch.mm(x, y.t()) / x.shape[1]