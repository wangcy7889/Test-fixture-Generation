import json
from typing import Optional
from datetime import datetime
from flask import Response

def http_error(status_code: int, title: Optional[str]=None, detail: Optional[str]=None):
    if title is None:
        title = 'Error'
    if detail is None:
        if 400 <= status_code < 500:
            detail = 'A client error occurred. Please check your request and try again.'
        elif 500 <= status_code < 600:
            detail = 'A server error occurred. Please try again later.'
        else:
            detail = 'An error occurred while processing the request. Please try again later.'
    return Response(response=json.dumps({'title': title, 'detail': detail, 'timestamp': str(datetime.now())}), status=status_code, headers={'Content-Type': 'application/problem+json'})