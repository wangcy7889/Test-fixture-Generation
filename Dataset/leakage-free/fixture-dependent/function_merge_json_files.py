
import os, json
from pathlib import Path
from typing import List, Dict, Any

def merge_json_files(json_paths: List[str],
                     env_out: str = 'MERGED_JSON') -> str:
    out_path = os.getenv(env_out)
    if not out_path:
        raise EnvironmentError('Error: MERGED_JSON is not set')
    merged: Dict[str, Any] = {}
    for p in json_paths:
        fp = Path(p)
        if not fp.is_file():
            raise FileNotFoundError(f"Error: '{p}' is not found")
        obj = json.loads(fp.read_text(encoding='utf-8'))
        if not isinstance(obj, dict):
            raise ValueError('Error: JSON is not a dictionary')
        merged.update(obj)
    Path(out_path).write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding='utf-8')
    return Path(out_path).resolve().as_posix()
