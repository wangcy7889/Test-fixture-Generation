
import os, time, shutil
from pathlib import Path

def clean_temp_files(env_temp: str = 'TEMP_DIR',
                     max_age_hours: int = 24) -> int:

    temp_root = os.getenv(env_temp)
    if not temp_root:
        raise EnvironmentError(f"Error: {env_temp} is not set")
    root = Path(temp_root)
    if not root.is_dir():
        raise FileNotFoundError(f"Error: '{temp_root}' is not found")

    cutoff = time.time() - max_age_hours*3600
    deleted = 0
    for p in root.iterdir():
        if p.is_file() and p.stat().st_mtime < cutoff:
            p.unlink()
            deleted +=1
        elif p.is_dir() and p.stat().st_mtime < cutoff:
            shutil.rmtree(p)
            deleted +=1
    return deleted
