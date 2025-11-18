from __future__ import annotations
from rich.errors import StyleSyntaxError
from rich.style import Style

def is_valid_style(style: str) -> bool:
    try:
        Style.parse(style)
        return True
    except StyleSyntaxError:
        return False