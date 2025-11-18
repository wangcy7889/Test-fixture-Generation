import os
from pathlib import Path
import configparser


def update_ini_setting(section: str, key: str, value: str) -> str:
    ini_path = os.getenv("CONFIG_INI")
    if not ini_path:
        raise EnvironmentError("Error: CONFIG_INI Not set")

    p = Path(ini_path)
    if not p.exists():
        raise FileNotFoundError(f"Error: {ini_path} not existed")

    cp = configparser.ConfigParser()
    cp.read(p, encoding="utf-8")

    if section not in cp:
        raise KeyError(f"Error: section '{section}' not existed")

    cp[section][key] = value
    with p.open("w", encoding="utf-8") as f:
        cp.write(f)

    return str(p.resolve())
