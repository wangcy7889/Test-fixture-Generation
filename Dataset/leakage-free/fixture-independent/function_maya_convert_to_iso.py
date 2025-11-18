import maya
from typing import Optional


def convert_to_iso(date_str: str, timezone_offset: Optional[int] = None) -> str:
    if timezone_offset is None:
        raise ValueError("Error: timezone_offset is required (between -12 and +14)")

    if not isinstance(timezone_offset, int) or not -12 <= timezone_offset <= 14:
        raise ValueError("Error: timezone_offset must be an integer between -12 and +14")

    try:
        m_date = maya.parse(date_str)
        m_date = m_date.add(hours=timezone_offset)
        return m_date.iso8601()
    except Exception as e:
        raise ValueError(f"Error: Unresolvable date: {date_str}") from e


