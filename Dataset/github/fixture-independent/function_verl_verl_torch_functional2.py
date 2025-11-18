from typing import Optional, Tuple
import torch

def _fused_linear_for_ppo_bwd(dlog_probs: Optional[torch.FloatTensor], dentropy: Optional[torch.FloatTensor], hidden_states: torch.FloatTensor, vocab_weights: torch.FloatTensor, input_ids: torch.LongTensor, temperature: float=1.0) -> Tuple[torch.FloatTensor, torch.FloatTensor]:
    logits = hidden_states @ vocab_weights.t() / temperature
    orig_dtype = logits.dtype
    logits = logits.to(torch.float32)
    probs = logits.softmax(dim=-1)
    dlogits = 0
    if dlog_probs is not None:
        one_hot_input = torch.zeros_like(logits).scatter_(-1, input_ids.unsqueeze(-1), 1)
        dlogits += dlog_probs.to(torch.float32).unsqueeze(-1) * (one_hot_input - probs)
    if dentropy is not None:
        log_probs = logits.log_softmax(dim=-1)
        entropy = torch.logsumexp(logits, dim=-1) - torch.sum(probs * logits, dim=-1)
        dlogits += probs * (log_probs + entropy.unsqueeze(-1)) * -dentropy.unsqueeze(-1)
    dlogits = dlogits.to(orig_dtype) / temperature
    dhidden_states = dlogits @ vocab_weights
    dvocab_weights = dlogits.t() @ hidden_states
    return (dhidden_states, dvocab_weights)