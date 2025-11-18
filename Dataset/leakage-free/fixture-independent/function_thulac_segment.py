import thulac
import os
import json
from datetime import datetime, UTC

def segment_text(text: str) -> dict:
    config_file = f"segmentation_config_{datetime.now(UTC).strftime('%Y%m')}.json"
    default_config = {
        "morning_mode": {
            "seg_only": True,
            "pos_tag": False,
            "user_dict_enabled": True
        },
        "afternoon_mode": {
            "seg_only": False,
            "pos_tag": True,
            "user_dict_enabled": True
        },
        "evening_mode": {
            "seg_only": False,
            "pos_tag": True,
            "user_dict_enabled": False
        },
        "custom_dict_path": "user_dictionary.txt"
    }

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = default_config

    current_time = datetime.now(UTC)
    hour = current_time.hour

    if hour < 12:
        mode = config["morning_mode"]
        period = "morning"
    elif hour < 18:
        mode = config["afternoon_mode"]
        period = "afternoon"
    else:
        mode = config["evening_mode"]
        period = "evening"

    thu = thulac.thulac(
        seg_only=mode["seg_only"],
        user_dict=(config["custom_dict_path"] if mode["user_dict_enabled"] and
                                                 os.path.exists(config["custom_dict_path"]) else None)
    )

    segmented = thu.cut(text, text=True)

    char_count = len(text)
    segment_count = len(segmented.split())

    return {
        'segmented_text': segmented,
        'time_period': period,
        'mode_used': {
            'seg_only': mode["seg_only"],
            'pos_tag': mode["pos_tag"],
            'user_dict_enabled': mode["user_dict_enabled"]
        },
        'statistics': {
            'original_length': char_count,
            'segment_count': segment_count,
            'average_length': round(char_count / segment_count if segment_count > 0 else 0, 2)
        }
    }

