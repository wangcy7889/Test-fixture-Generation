import sqlite3
from pathlib import Path

_DB = Path("metrics.db")

def increment_page_view(page: str) -> int:
    if not _DB.exists():
        raise FileNotFoundError("Error: metrics.db lost")

    conn = sqlite3.connect(_DB)
    try:
        conn.execute("INSERT OR IGNORE INTO counter(page, hits) VALUES (?, 0)", (page,))
        conn.execute("UPDATE counter SET hits = hits + 1 WHERE page = ?", (page,))
        conn.commit()
        hits, = conn.execute("SELECT hits FROM counter WHERE page = ?", (page,)).fetchone()
        return hits
    finally:
        conn.close()
