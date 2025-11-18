import torch
import os

def get_rank():
    print(os.environ.keys())
    if 'SLURM_PROCID' in os.environ:
        return int(os.environ['SLURM_PROCID'])
    if not torch.distributed.is_available() or not torch.distributed.is_initialized():
        return 0
    return torch.distributed.get_rank()