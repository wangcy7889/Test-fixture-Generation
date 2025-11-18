from torch import nn

def Downsample1d_2(in_channels: int, out_channels: int, factor: int, kernel_multiplier: int=2) -> nn.Module:
    assert kernel_multiplier % 2 == 0, 'Kernel multiplier must be even'
    return nn.Conv1d(in_channels=in_channels, out_channels=out_channels, kernel_size=factor * kernel_multiplier + 1, stride=factor, padding=factor * (kernel_multiplier // 2))