import os
import requests
STOCK_CODE_PATH = os.path.join(os.path.dirname(__file__), 'stock_codes.conf')

def update_stock_codes():
    response = requests.get('https://shidenggui.com/easy/stock_codes.json', headers={'Accept-Encoding': 'gzip'})
    with open(STOCK_CODE_PATH, 'w') as f:
        f.write(response.text)
    return response.json()