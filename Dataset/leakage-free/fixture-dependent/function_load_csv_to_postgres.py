
import csv
import os
from pathlib import Path
from typing import List

import psycopg2


def load_csv_to_postgres(csv_path: str,
                         table: str = "csv_import") -> int:
    dsn = os.getenv("PG_DSN")
    if not dsn:
        raise EnvironmentError("Error: PG_DSN is not set")

    csv_file = Path(csv_path)
    if not csv_file.is_file():
        raise FileNotFoundError(f"Error: {csv_path} is not a file")

    with csv_file.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise ValueError("Error: CSV is empty")
    header, *data_rows = rows

    conn = psycopg2.connect(dsn)
    try:
        with conn:
            with conn.cursor() as cur:
                # 建表（所有列类型 TEXT）
                cols_ddl = ", ".join(f'"{c}" TEXT' for c in header)
                cur.execute(f"""CREATE TABLE IF NOT EXISTS {table}
                               ({cols_ddl})""")
                # 插入行
                for r in data_rows:
                    placeholders = ", ".join(["%s"] * len(r))
                    cur.execute(f'INSERT INTO {table} VALUES ({placeholders})', r)
        conn.commit()
    finally:
        conn.close()

    return len(data_rows)
