import torch
from tqdm import trange, tqdm
import torch.distributions as dist

def truncated_logistic_normal_rescaled(shape, left_trunc=0.075, right_trunc=1):
    logits = torch.randn(shape)
    normal_dist = dist.Normal(0, 1)
    cdf_values = normal_dist.cdf(logits)
    lower_bound = normal_dist.cdf(torch.logit(torch.tensor(left_trunc)))
    upper_bound = normal_dist.cdf(torch.logit(torch.tensor(right_trunc)))
    truncated_cdf_values = lower_bound + (upper_bound - lower_bound) * cdf_values
    truncated_samples = torch.sigmoid(normal_dist.icdf(truncated_cdf_values))
    rescaled_samples = (truncated_samples - left_trunc) / (right_trunc - left_trunc)
    return rescaled_samples