
import os
import psycopg2
from typing import List

def pg_truncate_tables(tables: List[str],
                       env_dsn: str = 'PG_DSN') -> int:

    dsn = os.getenv(env_dsn)
    if not dsn:
        raise EnvironmentError('Error: PG_DSN is not set')
    if not tables:
        raise ValueError('Error: tables is empty')
    conn = psycopg2.connect(dsn)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute('TRUNCATE ' + ', '.join(tables) + ' RESTART IDENTITY CASCADE')
        return len(tables)
    finally:
        conn.close()
