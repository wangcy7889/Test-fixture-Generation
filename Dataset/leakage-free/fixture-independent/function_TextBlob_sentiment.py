from textblob import TextBlob
import os
import json
from datetime import datetime, UTC


def get_sentiment(text: str) -> dict:

    config_file = "sentiment_config.json"
    default_config = {
        "weekend_boost": 0.1,
        "workday_damping": 0.2,
        "morning_factor": 1.2,
        "evening_factor": 0.8,
        "polarity_threshold": 0.3,
        "subjectivity_threshold": 0.5
    }

    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = default_config

    current_time = datetime.now(UTC)
    is_weekend = current_time.weekday() >= 5
    is_morning = current_time.hour < 12

    blob = TextBlob(text)
    base_sentiment = blob.sentiment

    time_factor = (config['weekend_boost'] if is_weekend else -config['workday_damping'])
    hour_factor = config['morning_factor'] if is_morning else config['evening_factor']

    adjusted_polarity = min(1.0, max(-1.0, base_sentiment.polarity + time_factor)) * hour_factor
    adjusted_subjectivity = min(1.0, max(0.0, base_sentiment.subjectivity * hour_factor))

    return {
        'polarity': adjusted_polarity,
        'subjectivity': adjusted_subjectivity,
        'exceeds_threshold': abs(adjusted_polarity) > config['polarity_threshold']
                             and adjusted_subjectivity > config['subjectivity_threshold']
    }
