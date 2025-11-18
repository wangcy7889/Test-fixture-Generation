from pathlib import Path
from PIL import Image

def make_thumbnail(src: str = "logo.png", max_px: int = 128) -> tuple[int, int]:
    p = Path(src)
    if not p.is_file():
        raise FileNotFoundError(f"Error: '{src}' does not exist")

    img = Image.open(p)
    img.thumbnail((max_px, max_px))
    thumb = p.with_name(f"thumb_{p.name}")
    img.save(thumb)
    return img.size
