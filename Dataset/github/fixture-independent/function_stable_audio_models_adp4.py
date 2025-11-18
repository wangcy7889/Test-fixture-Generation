import torch.nn as nn

def FeedForward(features: int, multiplier: int) -> nn.Module:
    mid_features = features * multiplier
    return nn.Sequential(nn.Linear(in_features=features, out_features=mid_features), nn.GELU(), nn.Linear(in_features=mid_features, out_features=features))