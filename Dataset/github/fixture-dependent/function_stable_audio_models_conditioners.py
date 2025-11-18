import torch

def clap_load_state_dict(clap_ckpt_path, clap_model):
    state_dict = torch.load(clap_ckpt_path, map_location='cpu', weights_only=False)['state_dict']
    state_dict = {k[7:]: v for k, v in state_dict.items()}
    removed_keys = ['text_branch.embeddings.position_ids']
    for removed_key in removed_keys:
        if removed_key in state_dict:
            del state_dict[removed_key]
    clap_model.load_state_dict(state_dict, strict=False)