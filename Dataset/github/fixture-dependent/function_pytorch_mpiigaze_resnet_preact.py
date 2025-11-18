import torch
import torch.nn as nn

def _make_stage(in_channels: int, out_channels: int, n_blocks: int, block: torch.nn.Module, stride: int) -> torch.nn.Module:
    stage = nn.Sequential()
    for index in range(n_blocks):
        block_name = f'block{index + 1}'
        if index == 0:
            stage.add_module(block_name, block(in_channels, out_channels, stride=stride))
        else:
            stage.add_module(block_name, block(out_channels, out_channels, stride=1))
    return stage