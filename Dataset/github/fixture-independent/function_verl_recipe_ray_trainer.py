import torch

def softmean(x: torch.Tensor, beta: float, dim: int=-1, keepdim: bool=False) -> torch.Tensor:
    if beta == 0.0:
        return x.mean(dim=dim, keepdim=keepdim)
    beta_t = x.new_tensor(beta)
    lse = torch.logsumexp(x * beta_t, dim=dim, keepdim=keepdim)
    n = x.size(dim)
    log_n = x.new_tensor(n).log()
    return (lse - log_n) / beta_t