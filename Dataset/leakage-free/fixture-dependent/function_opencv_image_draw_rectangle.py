import cv2

def draw_rectangle_on_image(image_obj, rectangle_obj, color_obj, thickness_obj):

    if not (isinstance(rectangle_obj, tuple) and len(rectangle_obj) == 4):
        raise ValueError("Error: rectangle_obj must be (x, y, w, h) Tuple，from cv2.selectROI gained")
    if not isinstance(thickness_obj, int) or thickness_obj < 1:
        raise ValueError("Error: thickness_obj must be a positive integer，from cv2.getTrackbarPos gained")

    x, y, w, h = rectangle_obj
    pt1 = (int(x), int(y))
    pt2 = (int(x + w), int(y + h))
    img_copy = image_obj.copy()
    cv2.rectangle(img_copy, pt1, pt2, tuple(int(c) for c in color_obj), thickness_obj)
    return img_copy

