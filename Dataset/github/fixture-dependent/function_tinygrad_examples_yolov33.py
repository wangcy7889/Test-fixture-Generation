import numpy as np
from PIL import Image
from tinygrad.tensor import Tensor

def infer(model, img):
    img = np.array(Image.fromarray(img).resize((608, 608)))
    img = img[:, :, ::-1].transpose((2, 0, 1))
    img = img[np.newaxis, :, :, :] / 255.0
    prediction = model.forward(Tensor(img.astype(np.float32)))
    return prediction