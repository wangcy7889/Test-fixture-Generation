
import os, requests
from pathlib import Path

def slack_upload_file(file_path: str,
                      channels: str,
                      env_token: str = 'SLACK_BOT_TOKEN') -> str:
    token = os.getenv(env_token)
    if not token:
        raise EnvironmentError('Error: SLACK_BOT_TOKEN is not set')
    fp = Path(file_path)
    if not fp.is_file():
        raise FileNotFoundError(f"Error: file not found: {file_path}")
    url = 'https://slack.com/api/files.upload'
    with fp.open('rb') as f:
        resp = requests.post(url,
                             headers={'Authorization': f'Bearer {token}'},
                             files={'file': (fp.name, f)},
                             data={'channels': channels})
    if resp.status_code != 200 or not resp.json().get('ok'):
        raise RuntimeError('Error: Slack API error')
    return resp.json()['file']['permalink']
