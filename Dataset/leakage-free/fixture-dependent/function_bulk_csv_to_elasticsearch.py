
import os, csv, json, requests
from pathlib import Path
from typing import List

def bulk_csv_to_elasticsearch(csv_path: str,
                              index: str,
                              env_host: str = 'ES_HOST') -> int:
    host = os.getenv(env_host)
    if not host:
        raise EnvironmentError('Error: ES_HOST is not set')
    fp = Path(csv_path)
    if not fp.is_file():
        raise FileNotFoundError(f"Error: '{csv_path}' is not found")

    rows=[]
    with fp.open(newline='', encoding='utf-8') as f:
        reader=csv.DictReader(f)
        for r in reader:
            rows.append(r)
    if not rows:
        raise ValueError('Error: CSV is empty')

    ndjson_lines=[]
    for r in rows:
        ndjson_lines.append(json.dumps({'index': {'_index': index, '_id': r['id']}}))
        ndjson_lines.append(json.dumps({'text': r['text']}))
    payload='\n'.join(ndjson_lines)+'\n'
    url=f"{host}/_bulk"
    resp=requests.post(url, data=payload.encode(), headers={'Content-Type':'application/x-ndjson'})
    if resp.status_code!=200:
        raise RuntimeError('Error: HTTP error')
    res=resp.json()
    if res.get('errors'):
        raise RuntimeError('Error: Bulk errors')
    return len(rows)
