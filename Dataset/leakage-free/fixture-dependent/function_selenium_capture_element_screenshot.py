from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

def capture_element_screenshot(driver: WebDriver, element: WebElement, file_path: object) -> bool:
    if not hasattr(file_path, 'write') or not callable(file_path.write):
        raise TypeError("Error: file_path It must be a custom object that implements the write(bytes) method")
    try:
        png_bytes = element.screenshot_as_png
        file_path.write(png_bytes)
        return True
    except Exception:
        return False

