from PIL import ImageChops
from PIL.Image import Image


def calculate_image_diff(image1, image2):
    if not isinstance(image1, Image) or not isinstance(image2, Image):
        raise TypeError("Both arguments must be PIL.Image objects")
    if image1.size != image2.size or image1.mode != image2.mode:
        raise ValueError("Error: The size and mode of the two pictures must be the same")
    diff = ImageChops.difference(image1, image2)
    diff_data = diff.getdata()
    if diff.mode in ("RGB", "RGBA"):
        diff_pixels = sum(1 for px in diff_data if any(channel != 0 for channel in px))
    else:
        diff_pixels = sum(1 for px in diff_data if px != 0)
    return diff_pixels