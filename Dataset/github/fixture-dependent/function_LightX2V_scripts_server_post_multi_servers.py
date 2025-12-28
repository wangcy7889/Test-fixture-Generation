import requests
from loguru import logger
def get_available_urls(urls):
    available_urls = []
    for url in urls:
        try:
            _ = requests.get(f"{url}/v1/service/status").json()
            available_urls.append(url)
        except Exception as e:
            continue
    if not available_urls:
        logger.error("No available urls.")
        return None
    logger.info(f"available_urls: {available_urls}")
    return available_urls

