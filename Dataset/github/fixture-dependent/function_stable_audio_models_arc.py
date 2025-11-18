import torch.nn.functional as F

def get_relativistic_losses(score_real, score_fake):
    diff = score_real - score_fake
    dis_loss = F.softplus(-diff).mean()
    gen_loss = F.softplus(diff).mean()
    return (dis_loss, gen_loss)