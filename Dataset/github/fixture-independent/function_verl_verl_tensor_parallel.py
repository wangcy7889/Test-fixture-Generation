import torch

def get_default_kwargs_for_model_parallel_config():
    model_parallel_config_kwargs = {'params_dtype': torch.float32, 'use_cpu_initialization': False, 'perform_initialization': True, 'gradient_accumulation_fusion': False, 'sequence_parallel': False}
    return model_parallel_config_kwargs