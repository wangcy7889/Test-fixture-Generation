
import os
from pathlib import Path
from typing import Tuple
from PIL import Image

def resize_images_in_dir(src_dir: str,
                         size: Tuple[int,int] = (128,128),
                         env_out: str = 'RESIZED_DIR') -> int:
    out_dir_env = os.getenv(env_out)
    if not out_dir_env:
        raise EnvironmentError(f"Error: {env_out} is not set")
    out_dir = Path(out_dir_env)
    out_dir.mkdir(parents=True, exist_ok=True)

    root = Path(src_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Error: {src_dir} is not found")

    count = 0
    for img in root.iterdir():
        if img.suffix.lower() not in {'.jpg','.jpeg','.png'}:
            continue
        with Image.open(img) as im:
            im = im.copy()
            im.thumbnail(size)
            im.save(out_dir / img.name)
            count +=1
    if count==0:
        raise ValueError('Error: no images found')
    return count
