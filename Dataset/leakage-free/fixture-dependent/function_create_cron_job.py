
import os
from pathlib import Path

def create_cron_job(name: str,
                    schedule: str,
                    command: str,
                    env_dir: str = 'CRON_DIR') -> str:
    cron_dir = os.getenv(env_dir)
    if not cron_dir:
        raise EnvironmentError('Error: CRON_DIR is not set')
    d = Path(cron_dir)
    d.mkdir(parents=True, exist_ok=True)
    content = f"{schedule} {command}\n"
    path = d / f"{name}.cron"
    path.write_text(content, encoding='utf-8')
    return path.resolve().as_posix()
