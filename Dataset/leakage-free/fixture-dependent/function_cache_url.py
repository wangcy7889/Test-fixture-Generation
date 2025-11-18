
import os
from pathlib import Path
import requests


def cache_url(url: str,
              cache_dir_env: str = "CACHE_DIR",
              ttl_seconds: int = 3600) -> str:
    cache_dir = os.getenv(cache_dir_env)
    if not cache_dir:
        raise EnvironmentError(f"Error: {cache_dir_env} is not set")

    root = Path(cache_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Error:'{cache_dir}' is not found")

    fname = Path(url.split('/')[-1] or 'index.html')
    cache_file = root / fname

    # 若缓存有效
    if cache_file.exists() and (Path.cwd().stat().st_mtime - cache_file.stat().st_mtime) < ttl_seconds:
        return str(cache_file)

    resp = requests.get(url, timeout=5)
    if resp.status_code // 100 != 2:
        raise RuntimeError(f"Error: download fail: {resp.status_code}")
    cache_file.write_bytes(resp.content)
    return str(cache_file.resolve())
