
import os, subprocess, shlex
from pathlib import Path

def create_password_zip(src_dir: str,
                        zip_path: str,
                        env_pwd: str = 'ZIP_PASSWORD',
                        bin_env: str = 'ZIP_BIN') -> str:
    pwd=os.getenv(env_pwd)
    if not pwd:
        raise EnvironmentError('Error: ZIP_PASSWORD is not set')
    zip_bin=os.getenv(bin_env,'zip')
    root=Path(src_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Error: '{src_dir}' is not found")
    cmd=[zip_bin,'-r','-P',pwd,zip_path,'.']
    res=subprocess.run(cmd, cwd=str(root), capture_output=True, text=True)
    if res.returncode!=0:
        raise RuntimeError('Error: zip failed:'+res.stderr.strip())
    return str(Path(zip_path).resolve())
