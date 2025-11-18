import numpy as np
import time
import logging
import torch

def validate(val_loader, model, criterion, epoch):
    model.eval()
    end = time.time()
    with torch.no_grad():
        losses = []
        for i, (input, target) in enumerate(val_loader):
            target.requires_grad = False
            target = target.cuda(non_blocking=True)
            output = model(input)
            loss = criterion(output, target)
            losses.append(loss.item())
        elapse = time.time() - end
        loss = np.mean(losses)
        logging.info(f'Val: [{epoch}][{len(val_loader)}]\tLoss {loss:.4f}\tTime {elapse:.3f}')