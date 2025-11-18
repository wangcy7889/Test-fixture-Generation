import doctest
import requests

def _is_holiday(day):
    api = 'http://www.easybots.cn/api/holiday.php'
    params = {'d': day}
    rep = requests.get(api, params)
    res = rep.json()[day if isinstance(day, str) else day[0]]
    return True if res == '1' else False