from delorean import Delorean
from datetime import datetime
from typing import Optional
import pytz


def get_time_in_timezone(timezone: str, specific_date: Optional[datetime] = None, hour_only: bool = False) -> dict:
    try:
        tz = pytz.timezone(timezone)

        if specific_date:
            if specific_date.tzinfo is None:
                specific_date = pytz.UTC.localize(specific_date)
            d = Delorean(datetime=specific_date, timezone='UTC')
        else:
            d = Delorean()

        d.shift(timezone)

        result = {
            'timezone': timezone,
            'datetime': d.datetime,
            'date': d.date,
            'formatted_datetime': d.datetime.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'timezone_abbreviation': d.datetime.tzname()
        }

        if hour_only:
            result['hour'] = d.datetime.hour

        return result

    except Exception as e:
        raise ValueError(f"Error: Invalid timezone or date format: {str(e)}")

