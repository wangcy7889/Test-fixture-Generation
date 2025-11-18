from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from PIL import Image
import torch
from einops import rearrange
import numpy as np

def tokens_spectrogram_image(tokens, aspect='auto', title='Embeddings', ylabel='index', cmap='coolwarm', symmetric=True, figsize=(8, 4), dpi=100, mark_batches=False, debug=False):
    batch_size, dim, samples = tokens.shape
    embeddings = rearrange(tokens, 'b d n -> (b n) d')
    vmin, vmax = (None, None)
    if symmetric:
        vmax = torch.abs(embeddings).max()
        vmin = -vmax
    fig = Figure(figsize=figsize, dpi=dpi)
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_subplot()
    if symmetric:
        subtitle = f'min={embeddings.min():0.4g}, max={embeddings.max():0.4g}'
        ax.set_title(title + '\n')
        ax.text(x=0.435, y=0.9, s=subtitle, fontsize=11, ha='center', transform=fig.transFigure)
    else:
        ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('time frame (samples, in batches)')
    if mark_batches:
        intervals = np.arange(batch_size) * samples
        if debug:
            print('intervals = ', intervals)
        ax.vlines(intervals, -10, dim + 10, color='black', linestyle='dashed', linewidth=1)
    im = ax.imshow(embeddings.cpu().numpy().T, origin='lower', aspect=aspect, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    canvas.draw()
    rgba = np.asarray(canvas.buffer_rgba())
    return Image.fromarray(rgba)