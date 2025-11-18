
import os, json, requests, time
from pathlib import Path
from typing import List, Dict

def monitor_urls(urls: List[str],
                 env_out: str = 'STATUS_DIR',
                 timeout: int = 5) -> str:

    out_dir_path = os.getenv(env_out)
    if not out_dir_path:
        raise EnvironmentError(f"Error: {env_out} is not set")
    out_dir = Path(out_dir_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    report: Dict[str,int] = {}
    for u in urls:
        try:
            res = requests.get(u, timeout=timeout)
            report[u] = res.status_code
        except requests.RequestException:
            report[u] = 0
    fname = f"report_{int(time.time())}.json"
    fpath = out_dir / fname
    fpath.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return str(fpath.resolve())
