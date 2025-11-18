
import sqlite3
from pathlib import Path

def sqlite_run_script(db_path: str,
                      script_path: str) -> int:
    db = Path(db_path)
    if not db.is_file():
        raise FileNotFoundError(f"Error: file not found : {db_path}")
    script = Path(script_path)
    if not script.is_file():
        raise FileNotFoundError(f"Error: file not found : {script_path}")
    sql = script.read_text(encoding="utf-8")
    stmts = [s for s in sql.split(";") if s.strip()]
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        for stmt in stmts:
            cur.execute(stmt)
        conn.commit()
    finally:
        conn.close()
    return len(stmts)
