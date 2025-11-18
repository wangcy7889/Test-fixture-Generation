import os
import zipfile
from pathlib import Path
from typing import Tuple

from PIL import Image


def pack_thumbnails(src_dir: str,
                    zip_path: str = "thumbs.zip",
                    thumb_px: int = 64) -> Tuple[str, int]:
    root = Path(src_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Error: '{src_dir}' does not exist")

    imgs = [p for p in root.iterdir() if p.suffix.lower() in {".png", ".jpg", ".jpeg"}]
    if not imgs:
        raise ValueError("There are no pictures in the catalogue")

    quality = int(os.getenv("COMPRESS_QUALITY", "75"))
    out = Path(zip_path)
    count = 0

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in imgs:
            try:
                im = Image.open(p)
            except Exception:
                raise
            im.thumbnail((thumb_px, thumb_px))
            tmp = p.with_suffix(".thumb.jpg")
            im.save(tmp, "JPEG", quality=quality)
            zf.write(tmp, arcname=tmp.name)
            tmp.unlink()
            count += 1

    return str(out.resolve()), count
