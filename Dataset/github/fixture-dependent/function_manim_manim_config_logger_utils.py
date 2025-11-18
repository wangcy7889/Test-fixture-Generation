from __future__ import annotations
import configparser
from rich import color, errors
from rich import print as printf
from rich.theme import Theme
WRONG_COLOR_CONFIG_MSG = "\n[logging.level.error]Your colour configuration couldn't be parsed.\nLoading the default color configuration.[/logging.level.error]\n"

def parse_theme(parser: configparser.SectionProxy) -> Theme:
    theme = {key.replace('_', '.'): parser[key] for key in parser}
    theme['log.width'] = None if theme['log.width'] == '-1' else int(theme['log.width'])
    theme['log.height'] = None if theme['log.height'] == '-1' else int(theme['log.height'])
    theme['log.timestamps'] = False
    try:
        custom_theme = Theme({k: v for k, v in theme.items() if k not in ['log.width', 'log.height', 'log.timestamps']})
    except (color.ColorParseError, errors.StyleSyntaxError):
        printf(WRONG_COLOR_CONFIG_MSG)
        custom_theme = None
    return custom_theme