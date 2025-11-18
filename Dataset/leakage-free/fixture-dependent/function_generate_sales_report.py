import csv
import yaml
import psycopg2
from pathlib import Path
from typing import List

def generate_sales_report(
    year: int,
    cfg_path: str = "db.yaml",
    out_path: str | None = None
) -> str:
    cfg_file = Path(cfg_path)
    if not cfg_file.is_file():
        raise FileNotFoundError(f"Error: '{cfg_path}' does not exist")

    db_cfg = yaml.safe_load(cfg_file.read_text())
    conn = psycopg2.connect(**db_cfg)

    sql = """
        SELECT product_id,
               COUNT(*)  AS orders,
               SUM(price) AS revenue
        FROM   sales
        WHERE  EXTRACT(YEAR FROM created_at) = %s
        GROUP  BY product_id
        ORDER  BY revenue DESC;
    """

    with conn, conn.cursor() as cur:
        cur.execute(sql, (year,))
        rows: List[tuple] = cur.fetchall()

    if not out_path:
        out_path = f"{year}_sales.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "orders", "revenue"])
        writer.writerows(rows)

    return str(Path(out_path).resolve())
