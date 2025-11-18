
import os
import json
from typing import Dict, Any
import requests

def send_firebase_notification(token: str,
                               title: str,
                               body: str,
                               api_env: str = "FIREBASE_SERVER_KEY") -> Dict[str, Any]:
    key = os.getenv(api_env)
    if not key:
        raise EnvironmentError(f"Error: {api_env} is not defined")

    headers = {
        "Authorization": f"key={key}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": token,
        "notification": {"title": title, "body": body},
    }
    resp = requests.post("https://fcm.googleapis.com/fcm/send",
                         headers=headers, json=payload, timeout=5)
    if resp.status_code != 200:
        raise RuntimeError(f"Error: HTTP {resp.status_code}")
    js = resp.json()
    if js.get('failure'):
        raise RuntimeError('Error: FCM failure')
    return js
