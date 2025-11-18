import pyocr
import pyocr.builders
from PIL import Image

def extract_text_from_image(image_path: str) -> str:
    try:

        tools = pyocr.get_available_tools()
        if not tools:
            raise RuntimeError("Error: No OCR tool found")
        tool = tools[0]
        image = Image.open(image_path)
        text = tool.image_to_string(image, builder=pyocr.builders.TextBuilder())
        return text
    except Exception as e:
        raise e