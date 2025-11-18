import yaml
from pathlib import Path

def get_global_config() -> dict:
    config_dir = Path.home() / '.crawl4ai'
    config_file = config_dir / 'global.yml'
    if not config_file.exists():
        config_dir.mkdir(parents=True, exist_ok=True)
        return {}
    with open(config_file) as f:
        return yaml.safe_load(f) or {}