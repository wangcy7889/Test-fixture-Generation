from typing import Dict

import textdistance
import os
import json
from datetime import datetime, UTC


def compute_jaccard_similarity(str1: str, str2: str) -> dict[str, bool | int | float | str]:

    config_file = "similarity_config.json"
    default_config = {
        "morning_threshold": 0.3,
        "afternoon_threshold": 0.5,
        "evening_threshold": 0.7,
        "weekend_bonus": 0.1,
        "token_length_penalty": 0.05,
        "min_token_length": 3
    }

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = default_config

    current_time = datetime.now(UTC)
    hour = current_time.hour
    is_weekend = current_time.weekday() >= 5

    if hour < 12:
        threshold = config["morning_threshold"]
    elif hour < 18:
        threshold = config["afternoon_threshold"]
    else:
        threshold = config["evening_threshold"]

    tokens1 = [t for t in str1.split() if len(t) >= config["min_token_length"]]
    tokens2 = [t for t in str2.split() if len(t) >= config["min_token_length"]]

    base_similarity = textdistance.jaccard.normalized_similarity(tokens1, tokens2)

    adjusted_similarity = base_similarity

    if is_weekend:
        adjusted_similarity += config["weekend_bonus"]

    long_tokens = len([t for t in tokens1 + tokens2 if len(t) > 10])
    adjusted_similarity -= long_tokens * config["token_length_penalty"]

    final_similarity = max(0.0, min(1.0, adjusted_similarity))

    return {
        'similarity': final_similarity,
        'meets_threshold': final_similarity >= threshold,
        'threshold_used': threshold,
        'time_period': 'morning' if hour < 12 else 'afternoon' if hour < 18 else 'evening'
    }

