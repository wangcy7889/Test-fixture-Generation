import torch

def kl_penalty(logprob: torch.FloatTensor, ref_logprob: torch.FloatTensor, kl_penalty) -> torch.FloatTensor:
    if kl_penalty == 'kl':
        return logprob - ref_logprob
    if kl_penalty == 'abs':
        return (logprob - ref_logprob).abs()
    if kl_penalty == 'mse':
        return 0.5 * (logprob - ref_logprob).square()
    if kl_penalty == 'low_var_kl':
        kl = ref_logprob - logprob
        ratio = torch.exp(kl)
        kld = (ratio - kl - 1).contiguous()
        return torch.clamp(kld, min=-10, max=10)
    if kl_penalty == 'full':
        raise NotImplementedError
    raise NotImplementedError