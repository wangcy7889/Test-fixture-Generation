from typing import Tuple
import torch

def _fused_linear_for_ppo_fwd(hidden_states: torch.FloatTensor, vocab_weights: torch.FloatTensor, input_ids: torch.LongTensor, temperature: float=1.0) -> Tuple[torch.FloatTensor, torch.FloatTensor]:
    logits = hidden_states @ vocab_weights.t() / temperature
    orig_dtype = logits.dtype
    logits = logits.to(torch.float32)
    probs = logits.softmax(dim=-1)
    log_probs = logits.log_softmax(dim=-1)
    token_log_probs = log_probs.gather(-1, input_ids.unsqueeze(-1)).squeeze(-1)
    entropy = torch.logsumexp(logits, dim=-1) - torch.sum(probs * logits, dim=-1)
    return (token_log_probs.to(orig_dtype), entropy.to(orig_dtype))