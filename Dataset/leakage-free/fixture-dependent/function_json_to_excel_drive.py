
import os, json, tempfile, requests
from pathlib import Path
import openpyxl

def json_to_excel_drive(json_path: str,
                        env_url: str = 'DRIVE_UPLOAD_URL') -> str:
    upload_url = os.getenv(env_url)
    if not upload_url:
        raise EnvironmentError('Error: DRIVE_UPLOAD_URL is not set')
    jp = Path(json_path)
    if not jp.is_file():
        raise FileNotFoundError(f"Error: '{json_path}' is not found")
    data = json.loads(jp.read_text(encoding='utf-8'))
    if not isinstance(data, list):
        raise ValueError('Error: JSON top-level data must be a list')
    wb = openpyxl.Workbook()
    ws = wb.active
    if not data:
        raise ValueError('Error: JSON list data is empty')
    headers = list(data[0].keys())
    ws.append(headers)
    for row in data:
        ws.append([row.get(h) for h in headers])
    tmp = Path(tempfile.gettempdir())/('tmp.xlsx')
    wb.save(tmp)
    files = {'file': ('data.xlsx', tmp.open('rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    resp = requests.post(upload_url, files=files, timeout=10)
    if resp.status_code//100 != 2:
        raise RuntimeError('Error: upload failed')
    return 'uploaded'
