import json
from pathlib import Path
from typing import List

def merge_json_to_ndjson(src_dir: str,
                         out_path: str = "merged.ndjson") -> str:
    root = Path(src_dir)
    if not root.is_dir():
        raise FileNotFoundError(f"Error: '{src_dir}' does not exist")

    files: List[Path] = sorted(p for p in root.iterdir() if p.suffix == ".json")
    if not files:
        raise ValueError("Missing in the catalogue .json file")

    with Path(out_path).open("w", encoding="utf-8") as out_f:
        for fp in files:
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                raise ValueError(f"{fp} is not right JSON") from e
            out_f.write(json.dumps(data, separators=(",", ":")) + "\n")

    return str(Path(out_path).resolve())
