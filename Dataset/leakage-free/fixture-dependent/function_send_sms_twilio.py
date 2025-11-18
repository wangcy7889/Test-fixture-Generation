
import os, json, requests
from typing import Dict, Any

def send_sms_twilio(to_number: str,
                    body: str,
                    env_sid: str='TWILIO_SID',
                    env_token: str='TWILIO_TOKEN',
                    env_from: str='TWILIO_FROM') -> Dict[str, Any]:
    sid = os.getenv(env_sid); token = os.getenv(env_token); from_num = os.getenv(env_from)
    if not all([sid, token, from_num]):
        raise EnvironmentError('Error: Twilio environment variables not fully set')
    url = f'https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json'
    auth = (sid, token)
    data = {'From': from_num, 'To': to_number, 'Body': body}
    resp = requests.post(url, data=data, auth=auth, timeout=5)
    if resp.status_code != 201:
        raise RuntimeError(f'Error: HTTP {resp.status_code}')
    js = resp.json()
    if js.get('error_code'):
        raise RuntimeError('Error: Twilio error')
    return js
