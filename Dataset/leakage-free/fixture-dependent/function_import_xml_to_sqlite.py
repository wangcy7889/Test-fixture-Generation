
import os
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any


def import_xml_to_sqlite(xml_path: str,
                         table: str = "items",
                         env_db: str = "SQLITE_DB") -> int:
    db_file = os.getenv(env_db)
    if not db_file:
        raise EnvironmentError(f"Error: {env_db} is not set")
    xfile = Path(xml_path)
    if not xfile.is_file():
        raise FileNotFoundError(f"Error: {xml_path} is not a file")

    try:
        root = ET.fromstring(xfile.read_text(encoding='utf-8'))
    except ET.ParseError as e:
        raise ValueError('Error: XML is invalid') from e
    items = root.findall('.//item')
    if not items:
        raise ValueError('Error: XML has no valid <item>')
    rows = [(int(i.get('id')), i.get('name')) for i in items]

    conn = sqlite3.connect(db_file)
    try:
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, name TEXT)")
        conn.executemany(f"INSERT INTO {table}(id,name) VALUES (?,?) ON CONFLICT(id) DO UPDATE SET name=excluded.name", rows)
        conn.commit()
    finally:
        conn.close()
    return len(rows)
