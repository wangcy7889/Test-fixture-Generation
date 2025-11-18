
import os
import subprocess
from pathlib import Path

def gpg_encrypt_file(src_path: str,
                     recipient: str,
                     out_path: str | None = None,
                     bin_env: str = 'GPG_BIN') -> str:
    gpg = os.getenv(bin_env, 'gpg')
    src = Path(src_path)
    if not src.is_file():
        raise FileNotFoundError(f"'{src_path}' is not a file.")
    if out_path is None:
        out_path = str(src) + '.gpg'
    res = subprocess.run([gpg,'--batch','--yes','--output',out_path,
                          '--recipient',recipient,'--encrypt',str(src)],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Error: {res.stderr.strip()}")
    return Path(out_path).resolve().as_posix()
