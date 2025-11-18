import subprocess
from pathlib import Path

def current_commit_hash(repo: str = ".") -> str:
    if not Path(repo, ".git").exists():
        raise FileNotFoundError(f"Error: {repo} is not Git warehouse")

    res = subprocess.run(["git", "-C", repo, "rev-parse", "--short", "HEAD"],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError("git Command failed")
    return res.stdout.strip()
