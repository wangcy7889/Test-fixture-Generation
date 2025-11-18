import torch

def normalized_complex_distance_loss(x, y, eps=1e-07):
    numerator = torch.nn.functional.l1_loss(x, y, reduction='none').abs()
    denominator = 0.5 * (x.abs() + y.abs()) + eps
    return numerator / denominator