from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

def export_decision_makers(charts_dir: Path, csv_path: Path, threshold: float=0.5):
    rows = []
    for p in charts_dir.glob('org_chart_*.json'):
        data = json.loads(p.read_text())
        comp = p.stem.split('org_chart_')[1]
        for n in data.get('nodes', []):
            if n.get('decision_score', 0) >= threshold:
                rows.append(dict(company=comp, person=n['name'], title=n['title'], decision_score=n['decision_score'], profile_url=n['id']))
    pd.DataFrame(rows).to_csv(csv_path, index=False)