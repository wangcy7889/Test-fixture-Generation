
import os
import csv
from pathlib import Path
from typing import List

from reportlab.pdfgen import canvas


def generate_pdf_report(csv_path: str,
                        title: str = "Report",
                        env_out: str = "REPORT_OUTPUT_DIR") -> str:
    out_dir_env = os.getenv(env_out)
    if not out_dir_env:
        raise EnvironmentError(f"Error: {env_out} is not set")
    out_dir = Path(out_dir_env)
    if not out_dir.is_dir():
        raise FileNotFoundError(f"Error: {out_dir_env} is not found")

    cp = Path(csv_path)
    if not cp.is_file():
        raise FileNotFoundError(f"Error: {csv_path} is not found")

    rows: List[List[str]]
    with cp.open(newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))
    if len(reader) < 2:
        raise ValueError('Error: CSV should have at least two columns')

    pdf_path = out_dir / (cp.stem + '.pdf')
    c = canvas.Canvas(str(pdf_path))
    c.setTitle(title)

    x, y = 50, 800
    for row in reader:
        c.drawString(x, y, ' | '.join(row))
        y -= 20
    c.save()
    return str(pdf_path.resolve())
