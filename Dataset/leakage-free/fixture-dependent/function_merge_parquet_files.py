
import os, pyarrow.parquet as pq, pyarrow as pa
from pathlib import Path
from typing import List

def merge_parquet_files(files: List[str],
                        out_path: str,
                        env_tmp: str = 'PARQUET_TMP') -> str:

    tmp_dir = os.getenv(env_tmp)
    if not tmp_dir:
        raise EnvironmentError('Error: PARQUET_TMP is not set')
    Path(tmp_dir).mkdir(parents=True, exist_ok=True)

    tables=[]
    for f in files:
        p = Path(f)
        if not p.is_file():
            raise FileNotFoundError(f"Error: '{f}' is not found")
        tables.append(pq.read_table(p))
    combined = pa.concat_tables(tables)
    pq.write_table(combined, out_path)
    return str(Path(out_path).resolve())
