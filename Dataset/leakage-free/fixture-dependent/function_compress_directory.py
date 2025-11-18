
import os
import subprocess
from pathlib import Path

def compress_directory(dir_path: str,
                       tar_path: str = 'archive.tar.gz',
                       bin_env: str = 'TAR_BIN') -> str:

    tar_bin = os.getenv(bin_env, 'tar')
    root = Path(dir_path)
    if not root.is_dir():
        raise FileNotFoundError(f"Error: '{dir_path}' is not found")

    tar = Path(tar_path)
    res = subprocess.run([tar_bin, '-czf', str(tar), '-C', str(root.parent), root.name],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError('Error: tar failed: ' + res.stderr.strip())
    return str(tar.resolve())
