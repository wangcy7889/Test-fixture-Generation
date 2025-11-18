import requests
from colorama import Fore, Style

def is_ollama_available(ollama_url: str) -> bool:
    try:
        response = requests.get(f'{ollama_url}/api/version', timeout=5)
        if response.status_code == 200:
            return True
        print(f'{Fore.RED}Cannot connect to Ollama service at {ollama_url}.{Style.RESET_ALL}')
        print(f'{Fore.YELLOW}Make sure the Ollama service is running in your Docker environment.{Style.RESET_ALL}')
        return False
    except requests.RequestException as e:
        print(f'{Fore.RED}Error connecting to Ollama service: {e}{Style.RESET_ALL}')
        return False