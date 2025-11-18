import json
import subprocess
from pathlib import Path

def get_video_duration(src: str) -> float:
    path = Path(src)
    if not path.is_file():
        raise FileNotFoundError(f"Error: '{src}' does not exist")

    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
           "-show_format", str(path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError("ffprobe failed")

    meta = json.loads(res.stdout)
    return float(meta["format"]["duration"])
