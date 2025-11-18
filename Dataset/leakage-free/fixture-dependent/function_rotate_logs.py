
import os, gzip, shutil, time
from pathlib import Path

def rotate_logs(env_dir: str = 'APP_LOG_DIR',
                max_age_days: int = 7) -> int:
    log_dir = os.getenv(env_dir)
    if not log_dir:
        raise EnvironmentError('Error: APP_LOG_DIR is not set')
    root = Path(log_dir)
    if not root.is_dir():
        raise FileNotFoundError(log_dir)
    cutoff = time.time() - max_age_days*86400
    count=0
    for log in root.glob('*.log'):
        if log.stat().st_mtime < cutoff:
            gz = log.with_suffix(log.suffix+'.gz')
            with open(log, 'rb') as f_in, gzip.open(gz,'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            log.unlink()
            count+=1
    return count
