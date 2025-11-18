from typing import NamedTuple
import requests
from lxml import html

class CovidData(NamedTuple):
    cases: int
    deaths: int
    recovered: int

def covid_stats(url: str='https://www.worldometers.info/coronavirus/') -> CovidData:
    xpath_str = '//div[@class = "maincounter-number"]/span/text()'
    return CovidData(*html.fromstring(requests.get(url, timeout=10).content).xpath(xpath_str))