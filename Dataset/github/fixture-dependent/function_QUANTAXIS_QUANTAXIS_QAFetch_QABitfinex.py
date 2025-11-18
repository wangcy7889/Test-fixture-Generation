import requests
import json
import time
from requests.exceptions import ConnectTimeout, SSLError, ReadTimeout, ConnectionError
from retrying import retry
from urllib.parse import urljoin
TIMEOUT = 10
ILOVECHINA = '同学！！你知道什么叫做科学上网么？ 如果你不知道的话，那么就加油吧！蓝灯，喵帕斯，VPS，阴阳师，v2ray，随便什么来一个！我翻墙我骄傲！'
Bitfinex_base_url = 'https://api-pub.bitfinex.com/'

@retry(stop_max_attempt_number=3, wait_random_min=50, wait_random_max=100)
def QA_fetch_bitfinex_symbols():
    url = urljoin(Bitfinex_base_url, '/api/v1/exchangeInfo')
    retries = 1
    datas = list()
    while retries != 0:
        try:
            req = requests.get(url, timeout=TIMEOUT)
            retries = 0
        except (ConnectTimeout, ConnectionError, SSLError, ReadTimeout):
            retries = retries + 1
            if retries % 6 == 0:
                print(ILOVECHINA)
            print('Retry /api/v1/exchangeInfo #{}'.format(retries - 1))
            time.sleep(0.5)
        if retries == 0:
            symbol_lists = json.loads(req.content)
            if len(symbol_lists) == 0:
                return []
            for symbol in symbol_lists:
                datas.append(symbol)
    return datas