
import os, json, uuid, requests
from typing import Dict

def azure_translate_text(text: str,
                         target_lang: str = 'en',
                         env_key: str = 'AZURE_TRANSLATOR_KEY',
                         env_endpoint: str = 'AZURE_TRANSLATOR_ENDPOINT') -> Dict:
    key = os.getenv(env_key); endpoint = os.getenv(env_endpoint)
    if not all([key, endpoint]):
        raise EnvironmentError('Error: Azure Translator is not set')
    url = endpoint.rstrip('/') + '/translate?api-version=3.0&to=' + target_lang
    headers = {'Ocp-Apim-Subscription-Key': key,
               'Content-Type': 'application/json',
               'Ocp-Apim-Subscription-Region': 'global',
               'X-ClientTraceId': str(uuid.uuid4())}
    body = [{'text': text}]
    resp = requests.post(url, headers=headers, json=body, timeout=5)
    if resp.status_code != 200:
        raise RuntimeError(f'Error: HTTP {resp.status_code}')
    js = resp.json()
    if 'error' in js:
        raise RuntimeError('Error: Azure error')
    return js[0]['translations'][0]
