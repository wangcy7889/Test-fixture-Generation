import os
import json
from datetime import datetime, UTC

def write_log(log_directory: str, message: str) -> dict:
    config_file = "log_config.json"
    default_config = {
        "morning": {"format": "long", "max_size_mb": 10},
        "afternoon": {"format": "medium", "max_size_mb": 5},
        "evening": {"format": "short", "max_size_mb": 2}
    }

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = default_config

    current_time = datetime.now(UTC)
    period = ("morning" if current_time.hour < 12
             else "afternoon" if current_time.hour < 18
             else "evening")
    settings = config[period]

    if not os.path.exists(log_directory):
        raise FileNotFoundError("Error: Log directory does not exist")

    log_file = os.path.join(log_directory, f'log_{current_time.strftime("%Y%m%d")}_{period}.log')

    if settings["format"] == "long":
        log_line = f"{current_time.isoformat()} - {period} - {message}\n"
    elif settings["format"] == "medium":
        log_line = f"{current_time.strftime('%H:%M:%S')} - {message}\n"
    else:
        log_line = f"{current_time.strftime('%H:%M')} {message}\n"

    try:
        if os.path.exists(log_file) and os.path.getsize(log_file) >= settings["max_size_mb"] * 1024 * 1024:
            log_file = os.path.join(log_directory, f'log_{current_time.strftime("%Y%m%d_%H%M")}_{period}.log')

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_line)

        return {
            'file': log_file,
            'period': period,
            'format': settings["format"]
        }

    except IOError as e:
        raise IOError(f"Error: write failed {log_file}: {e}")