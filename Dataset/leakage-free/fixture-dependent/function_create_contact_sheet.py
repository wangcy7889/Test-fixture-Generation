from pathlib import Path
from typing import List
from PIL import Image

def create_contact_sheet(folder: str = "gallery",
                         thumb_px: int = 100,
                         columns: int = 4) -> str:
    root = Path(folder)
    if not root.is_dir():
        raise FileNotFoundError(f"Error: {folder} does not exist")

    imgs: List[Path] = sorted(p for p in root.iterdir() if p.is_file())
    if len(imgs) < columns:
        raise ValueError(f"Error: at least need {columns} pictures")

    thumbs = [Image.open(p).copy() for p in imgs]
    for im in thumbs:
        im.thumbnail((thumb_px, thumb_px))

    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_px, rows * thumb_px), "white")

    for idx, im in enumerate(thumbs):
        x = (idx % columns) * thumb_px
        y = (idx // columns) * thumb_px
        sheet.paste(im, (x, y))

    out = root / "contact_sheet.jpg"
    sheet.save(out)
    return str(out.resolve())
