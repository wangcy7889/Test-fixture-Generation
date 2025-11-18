from typing import Optional
import torch
import torch.utils.checkpoint

def _expand_mask(mask: torch.Tensor, dtype: torch.dtype, tgt_len: Optional[int]=None):
    bsz, src_len = mask.size()
    tgt_len = tgt_len if tgt_len is not None else src_len
    expanded_mask = mask[:, None, None, :].expand(bsz, 1, tgt_len, src_len).to(dtype)
    inverted_mask = 1.0 - expanded_mask
    return inverted_mask.masked_fill(inverted_mask.to(torch.bool), torch.finfo(dtype).min)