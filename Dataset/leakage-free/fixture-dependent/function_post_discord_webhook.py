
import os, json, requests
from typing import Dict

def post_discord_webhook(content: str,
                         username: str = 'Bot',
                         webhook_env: str = 'DISCORD_WEBHOOK') -> Dict:

    url = os.getenv(webhook_env)
    if not url:
        raise EnvironmentError(f"Error: {webhook_env} is not defined")
    data = {'username': username, 'content': content}
    resp = requests.post(url, json=data, timeout=5)
    if resp.status_code != 204:
        raise RuntimeError(f"Error: HTTP {resp.status_code}")
    return {'status':'sent'}
