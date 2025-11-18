import torch
import math

def build_mask(sample_size, mask_args):
    maskstart = math.floor(mask_args['maskstart'] / 100.0 * sample_size)
    maskend = math.ceil(mask_args['maskend'] / 100.0 * sample_size)
    softnessL = round(mask_args['softnessL'] / 100.0 * sample_size)
    softnessR = round(mask_args['softnessR'] / 100.0 * sample_size)
    marination = mask_args['marination']
    hannL = torch.hann_window(softnessL * 2, periodic=False)[:softnessL]
    hannR = torch.hann_window(softnessR * 2, periodic=False)[softnessR:]
    mask = torch.zeros(sample_size)
    mask[maskstart:maskend] = 1
    mask[maskstart:maskstart + softnessL] = hannL
    mask[maskend - softnessR:maskend] = hannR
    if marination > 0:
        mask = mask * (1 - marination)
    return mask