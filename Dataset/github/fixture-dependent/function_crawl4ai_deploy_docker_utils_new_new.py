import yaml
from pathlib import Path
from typing import Dict

def load_config() -> Dict:
    config_path = Path(__file__).parent / 'config.yml'
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)