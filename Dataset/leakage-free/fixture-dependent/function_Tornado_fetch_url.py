import tornado.httpclient
import tornado.gen
import os
import json
from datetime import datetime, UTC

@tornado.gen.coroutine
def fetch_url(url: str) -> dict:
    config_file = "fetch_config.json"
    default_config = {
        "timeout_settings": {
            "morning": 30,
            "afternoon": 20,
            "evening": 15
        },
        "retry_settings": {
            "morning": 3,
            "afternoon": 2,
            "evening": 1
        },
        "headers": {
            "User-Agent": "CustomFetcher/1.0",
            "Accept": "text/html,application/json"
        },
        "request_log_path": "request_history.json"
    }

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = default_config

    current_time = datetime.now(UTC)
    hour = current_time.hour

    if hour < 12:
        period = "morning"
    elif hour < 18:
        period = "afternoon"
    else:
        period = "evening"

    timeout = config["timeout_settings"][period]
    max_retries = config["retry_settings"][period]

    client = tornado.httpclient.AsyncHTTPClient()
    request = tornado.httpclient.HTTPRequest(
        url=url,
        connect_timeout=timeout,
        request_timeout=timeout,
        headers=config["headers"]
    )

    response = None
    errors = []
    for attempt in range(max_retries):
        try:
            response = yield client.fetch(request)
            break
        except Exception as e:
            errors.append(f"Attempt {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                raise

    request_log = {
        "timestamp": current_time.isoformat(),
        "url": url,
        "period": period,
        "timeout_used": timeout,
        "attempts_made": len(errors) + 1,
        "success": response is not None
    }

    history_file = config["request_log_path"]
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            history = json.load(f)
    history.append(request_log)
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)

    return {
        'content': response.body.decode('utf-8'),
        'metadata': {
            'status_code': response.code,
            'headers': dict(response.headers),
            'time_period': period,
            'attempts': len(errors) + 1,
            'final_url': response.effective_url
        }
    }

