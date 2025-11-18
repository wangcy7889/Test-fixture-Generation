from lassie import Lassie
from typing import Dict, Any
import logging


def extract_media_content(url: str, include_images: bool = True) -> Dict[Any, Any]:
    try:
        lassie_instance = Lassie()
        result = lassie_instance.fetch(
            url,
            all_images=include_images
        )
        return result
    except Exception as e:
        logging.error(f"Error extracting media content from {url}: {str(e)}")
        raise Exception(e)