import cv2
import numpy as np

def white_to_black(image_path, output_path=None, threshold=220):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Error: The picture cannot be read. Please check if the path is correct")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, threshold])
    upper_white = np.array([180, 30, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)

    hsv[mask > 0] = [0, 0, 0]

    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    if output_path is not None:
        cv2.imwrite(output_path, img)
    else:
        cv2.imwrite(image_path, img)

    return img