from xpinyin import Pinyin
import os
import json
from datetime import datetime, UTC


def convert_to_pinyin(text: str) -> dict:
    config_file = "pinyin_config.json"
    default_config = {
        "morning": {"tone": True, "sep": " "},
        "afternoon": {"tone": False, "sep": "-"},
        "evening": {"tone": False, "sep": "_"}
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

    p = Pinyin()
    result = p.get_pinyin(text, settings["sep"])

    if not settings["tone"]:
        result = ''.join([c for c in result if not c.isdigit()])

    return {
        'pinyin': result,
        'time_period': period,
        'settings': settings
    }


