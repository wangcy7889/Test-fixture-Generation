
import os, requests
from typing import Dict

def pushbullet_note(title: str,
                    body: str,
                    env_token: str = 'PUSHBULLET_TOKEN') -> Dict:
    token = os.getenv(env_token)
    if not token:
        raise EnvironmentError('Error: PUSHBULLET_TOKEN is not set')
    url = 'https://api.pushbullet.com/v2/pushes'
    headers = {'Access-Token': token, 'Content-Type': 'application/json'}
    resp = requests.post(url, json={'type':'note','title':title,'body':body}, headers=headers, timeout=5)
    if resp.status_code != 200:
        raise RuntimeError('Error: HTTP error')
    return resp.json()
