from PIL import Image
import io

def generate_thumbnail(image_bytes, size=(100, 100)):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.thumbnail(size)
        output = io.BytesIO()
        img.save(output, format="JPEG")
        return output.getvalue()
    except Exception as e:
        raise e