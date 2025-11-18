
import os
import subprocess
from pathlib import Path

def sync_git_repo(repo_url: str,
                  dest_dir: str,
                  bin_env: str = "GIT_BIN") -> str:
    git_bin = os.getenv(bin_env, "git")
    dest = Path(dest_dir).expanduser()
    if not dest.parent.exists():
        raise FileNotFoundError(f"Error: {dest.parent} does not exist" )

    if dest.exists():
        # pull
        cmd = [git_bin, "-C", str(dest), "pull", "--ff-only"]
    else:
        # clone
        cmd = [git_bin, "clone", repo_url, str(dest)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip() or "git error")
    return str(dest.resolve())
