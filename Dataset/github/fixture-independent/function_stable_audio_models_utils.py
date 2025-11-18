import torch

def copy_state_dict(model, state_dict):
    model_state_dict = model.state_dict()
    for key in state_dict:
        if key in model_state_dict and state_dict[key].shape == model_state_dict[key].shape:
            if isinstance(state_dict[key], torch.nn.Parameter):
                state_dict[key] = state_dict[key].data
            model_state_dict[key] = state_dict[key]
    model.load_state_dict(model_state_dict, strict=False)