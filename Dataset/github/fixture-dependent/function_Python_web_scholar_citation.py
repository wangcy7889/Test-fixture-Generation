import requests
from bs4 import BeautifulSoup

def get_citation(base_url: str, params: dict) -> str:
    soup = BeautifulSoup(requests.get(base_url, params=params, timeout=10).content, 'html.parser')
    div = soup.find('div', attrs={'class': 'gs_ri'})
    anchors = div.find('div', attrs={'class': 'gs_fl'}).find_all('a')
    return anchors[2].get_text()