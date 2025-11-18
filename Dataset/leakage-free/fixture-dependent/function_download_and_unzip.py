
import os, requests, zipfile, io
from pathlib import Path

def download_and_unzip(url: str,
                       env_dir: str = 'UNZIP_DIR') -> int:
    out_dir = os.getenv(env_dir)
    if not out_dir:
        raise EnvironmentError('Error: UNZIP_DIR is not set')
    dest = Path(out_dir)
    dest.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        raise RuntimeError('Error: Download failed')
    with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
        zf.extractall(dest)
        return len(zf.namelist())
