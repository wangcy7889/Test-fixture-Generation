import requests
from colorama import Fore, Style

def get_available_models(ollama_url: str) -> list:
    """Get list of available models in Docker environment."""
    try:
        response = requests.get(f'{ollama_url}/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [m['name'] for m in models]
        print(f'{Fore.RED}Failed to get available models from Ollama service. Status code: {response.status_code}{Style.RESET_ALL}')
        return []
    except requests.RequestException as e:
        print(f'{Fore.RED}Error getting available models: {e}{Style.RESET_ALL}')
        return []