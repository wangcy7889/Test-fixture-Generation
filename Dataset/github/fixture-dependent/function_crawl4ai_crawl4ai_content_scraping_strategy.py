import re
import requests
from urllib.parse import urljoin
from requests.exceptions import InvalidSchema
DIMENSION_REGEX = re.compile('(\\d+)(\\D*)')

def fetch_image_file_size(img, base_url):
    img_url = urljoin(base_url, img.get('src'))
    try:
        response = requests.head(img_url)
        if response.status_code == 200:
            return response.headers.get('Content-Length', None)
        else:
            print(f'Failed to retrieve file size for {img_url}')
            return None
    except InvalidSchema:
        return None
    finally:
        return