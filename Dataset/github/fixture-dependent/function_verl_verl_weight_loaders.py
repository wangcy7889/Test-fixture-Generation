import torch

def parallel_weight_loader(self, param: torch.Tensor, loaded_weight: torch.Tensor) -> None:
    assert param.size() == loaded_weight.size(), 'the parameter size is not align with the loaded weight size, param size: {}, loaded_weight size: {}'.format(param.size(), loaded_weight.size())
    assert param.data.dtype == loaded_weight.data.dtype, 'if we want to shared weights, the data type should also be the same'
    param.data = loaded_weight.data