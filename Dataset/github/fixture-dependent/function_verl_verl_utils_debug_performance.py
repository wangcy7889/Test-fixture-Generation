from typing import Tuple
import torch

def _get_current_mem_info(unit: str='GB', precision: int=2) -> Tuple[str]:
    assert unit in ['GB', 'MB', 'KB']
    divisor = 1024 ** 3 if unit == 'GB' else 1024 ** 2 if unit == 'MB' else 1024
    mem_allocated = torch.cuda.memory_allocated()
    mem_reserved = torch.cuda.memory_reserved()
    mem_free, mem_total = torch.cuda.mem_get_info()
    mem_used = mem_total - mem_free
    mem_allocated = f'{mem_allocated / divisor:.{precision}f}'
    mem_reserved = f'{mem_reserved / divisor:.{precision}f}'
    mem_used = f'{mem_used / divisor:.{precision}f}'
    mem_total = f'{mem_total / divisor:.{precision}f}'
    return (mem_allocated, mem_reserved, mem_used, mem_total)