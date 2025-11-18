import os
from pathlib import Path
from tinygrad.helpers import fetch

def download_weights(total_num_weights: int) -> Path:
    model = fetch('https://huggingface.co/Qwen/QwQ-32B-Preview/resolve/main/model.safetensors.index.json?download=true', 'model.safetensors.index.json', subdir=(subdir := 'qwq_32b_preview'))
    for i in range(1, total_num_weights + 1):
        filename = f'model-{i:05d}-of-{total_num_weights:05d}.safetensors'
        fetch(f'https://huggingface.co/Qwen/QwQ-32B-Preview/resolve/main/{filename}?download=true', filename, subdir=subdir)
    return Path(os.path.dirname(model))