
import os
import csv
import requests
from pathlib import Path
from typing import Dict, List

def push_metrics_from_csv(csv_path: str,
                          job: str = "csv_job",
                          label_column: str = "metric") -> Dict[str, str]:
    gateway = os.getenv("PUSHGATEWAY_URL")
    if not gateway:
        raise EnvironmentError("Error: PUSHGATEWAY_URL is not set")

    fp = Path(csv_path)
    if not fp.is_file():
        raise FileNotFoundError(f"Error: {csv_path} is not a file")

    lines: List[str] = []
    with fp.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if label_column not in reader.fieldnames or 'value' not in reader.fieldnames:
            raise ValueError("Error: CSV must contain '%s' and 'value' columns" % label_column)
        for row in reader:
            try:
                val = float(row['value'])
            except ValueError:
                raise ValueError("Error: value includes invalid number") from None
            metric_name = row[label_column]
            lines.append(f"{metric_name} {val}")

    payload = "\n".join(lines) + "\n"
    url = f"{gateway}/metrics/job/{job}"
    resp = requests.post(url, data=payload.encode(), timeout=5,
                         headers={"Content-Type": "text/plain"})
    if resp.status_code // 100 != 2:
        raise RuntimeError(f"Error: Pushgateway fail {resp.status_code}: {resp.text.strip()}")
    return {"status": "success", "code": resp.status_code}
