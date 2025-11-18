import requests
from colorama import Fore, Style

def delete_model(model_name: str, ollama_url: str) -> bool:
    print(f'{Fore.YELLOW}Deleting model {model_name} from Docker container...{Style.RESET_ALL}')
    try:
        response = requests.delete(f'{ollama_url}/api/delete', json={'name': model_name}, timeout=10)
        if response.status_code == 200:
            print(f'{Fore.GREEN}Model {model_name} deleted successfully.{Style.RESET_ALL}')
            return True
        else:
            print(f'{Fore.RED}Failed to delete model. Status code: {response.status_code}{Style.RESET_ALL}')
            if response.text:
                print(f'{Fore.RED}Error: {response.text}{Style.RESET_ALL}')
            return False
    except requests.RequestException as e:
        print(f'{Fore.RED}Error deleting model: {e}{Style.RESET_ALL}')
        return False