from __future__ import annotations
import sys
from typing import Any
if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

def get_plugins() -> dict[str, Any]:
    plugins: dict[str, Any] = {entry_point.name: entry_point.load() for entry_point in entry_points(group='manim.plugins')}
    return plugins