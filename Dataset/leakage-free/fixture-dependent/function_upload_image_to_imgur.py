
import os
from pathlib import Path
from typing import Dict, Any

import requests


def upload_image_to_imgur(image_path: str,
                          title: str | None = None,
                          description: str | None = None) -> Dict[str, Any]:
    cid = os.getenv("IMGUR_CLIENT_ID")
    if not cid:
        raise EnvironmentError("Error: IMGUR_CLIENT_ID is not set")

    img = Path(image_path)
    if not img.is_file():
        raise FileNotFoundError(f"Error: {image_path} is not a file")
    if img.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif"}:
        raise ValueError("Error: Unsupported image format")

    headers = {"Authorization": f"Client-ID {cid}"}
    data = {"title": title, "description": description}
    files = {"image": img.read_bytes()}
    resp = requests.post("https://api.imgur.com/3/image",
                         headers=headers,
                         data=data,
                         files=files,
                         timeout=10)

    if resp.status_code != 200:
        raise RuntimeError(f"Error: Imgur HTTP {resp.status_code}")
    js = resp.json()
    if not js.get("success"):
        raise RuntimeError("Error: Imgur API failed")
    return js
