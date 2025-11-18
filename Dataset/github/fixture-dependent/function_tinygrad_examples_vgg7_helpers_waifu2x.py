import numpy
from PIL import Image

def image_load(path) -> numpy.ndarray:
    na = numpy.array(Image.open(path))
    if na.shape[2] == 4:
        na = na[:, :, 0:3]
    na = numpy.moveaxis(na, [2, 0, 1], [0, 1, 2])
    na = na.reshape(1, 3, na.shape[1], na.shape[2])
    na = na.astype('float32') / 255.0
    return na