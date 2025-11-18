import gevent
from gevent import monkey
import requests
from typing import List, Dict
import logging


def download_urls(urls: List[str]) -> Dict[str, str]:

    def fetch_url(url: str) -> tuple:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return url, response.text
        except requests.RequestException as e:
            logging.error(f"Error downloading {url}: {str(e)}")
            raise requests.RequestException(e)
        except Exception as e:
            logging.error(f"Unexpected error for {url}: {str(e)}")
            raise Exception(e)

    monkey.patch_all()

    jobs = [gevent.spawn(fetch_url, url) for url in urls]

    gevent.joinall(jobs, timeout=15)

    results = {}
    for job in jobs:
        if job.value:
            url, content = job.value
            results[url] = content
        else:
            url = urls[jobs.index(job)]
            results[url] = "Error: Request timeout or failed"

    return results