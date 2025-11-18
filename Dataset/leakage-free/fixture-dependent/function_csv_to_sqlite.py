
import os, csv, sqlite3
from pathlib import Path

def csv_to_sqlite(csv_path: str,
                  table: str = 'data',
                  env_db: str = 'CSV_DB') -> int:
    db_file = os.getenv(env_db)
    if not db_file:
        raise EnvironmentError('Error: CSV_DB is not set')
    cp = Path(csv_path)
    if not cp.is_file():
        raise FileNotFoundError(f"Error: '{csv_path}' is not found")
    with cp.open(newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
    if len(reader) < 2:
        raise ValueError('Error: CSV must comtain at least two columns')
    header, rows = reader[0], reader[1:]
    conn = sqlite3.connect(db_file)
    try:
        cols = ', '.join(f'"{h}" TEXT' for h in header)
        conn.execute(f'CREATE TABLE IF NOT EXISTS {table} ({cols})')
        placeholders = ','.join(['?']*len(header))
        conn.executemany(f'INSERT INTO {table} VALUES ({placeholders})', rows)
        conn.commit()
    finally:
        conn.close()
    return len(rows)
