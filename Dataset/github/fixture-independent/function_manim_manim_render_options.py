from __future__ import annotations
import logging
import re
import sys
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from click import Context, Option
logger = logging.getLogger('manim')

def validate_resolution(ctx: Context, param: Option, value: str | None) -> tuple[int, int] | None:
    if value is None:
        return None
    try:
        width, height = map(int, re.split('[;,\\-]', value))
    except Exception:
        logger.error('Resolution option is invalid.')
        sys.exit()
    return (width, height)