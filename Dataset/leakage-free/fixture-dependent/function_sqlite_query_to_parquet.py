
import sqlite3, pyarrow as pa, pyarrow.parquet as pq
from pathlib import Path

def sqlite_query_to_parquet(db_path: str,
                            query: str,
                            out_path: str) -> str:
    db=Path(db_path)
    if not db.is_file():
        raise FileNotFoundError(f"Error: file not found: {db_path}")
    conn=sqlite3.connect(db_path)
    try:
        cur=conn.execute(query)
        rows=cur.fetchall()
        if not rows:
            raise ValueError('Error: No result')
        cols=[d[0] for d in cur.description]
    finally:
        conn.close()
    table=pa.Table.from_pylist([dict(zip(cols,r)) for r in rows])
    pq.write_table(table, out_path)
    return Path(out_path).resolve().as_posix()
