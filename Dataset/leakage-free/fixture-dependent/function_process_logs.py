
import os
import re
from pathlib import Path
from typing import Dict

def process_logs(pattern: str,
                 summary_path: str = "summary.txt",
                 env_dir: str = "LOG_ROOT") -> Dict[str, int]:

    root_dir = os.getenv(env_dir)
    if not root_dir:
        raise EnvironmentError(f"Error: {env_dir} is not set")
    root = Path(root_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Error: {root_dir} is not found")

    try:
        regex = re.compile(pattern)
    except re.error as e:
        raise ValueError("Error: invalid regex") from e

    counts = {}
    for log in root.glob("*.log"):
        text = log.read_text(encoding="utf-8", errors="ignore")
        counts[log.name] = len(regex.findall(text))

    if not counts:
        raise ValueError("Error: no logs found")

    out = Path(summary_path)
    lines = [f"{k}\t{v}" for k, v in counts.items()]
    out.write_text("\n".join(lines), encoding="utf-8")
    return counts
