import requests
BASE_URL = 'https://api.carbonintensity.org.uk/intensity'

def fetch_last_half_hour() -> str:
    last_half_hour = requests.get(BASE_URL, timeout=10).json()['data'][0]
    return last_half_hour['intensity']['actual']