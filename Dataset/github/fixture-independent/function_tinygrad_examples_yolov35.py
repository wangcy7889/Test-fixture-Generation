import numpy as np
from tinygrad.tensor import Tensor

def predict_transform(prediction, inp_dim, anchors, num_classes):
    batch_size = prediction.shape[0]
    stride = inp_dim // prediction.shape[2]
    grid_size = inp_dim // stride
    bbox_attrs = 5 + num_classes
    num_anchors = len(anchors)
    prediction = prediction.reshape(shape=(batch_size, bbox_attrs * num_anchors, grid_size * grid_size))
    prediction = prediction.transpose(1, 2)
    prediction = prediction.reshape(shape=(batch_size, grid_size * grid_size * num_anchors, bbox_attrs))
    prediction_cpu = prediction.numpy()
    for i in (0, 1, 4):
        prediction_cpu[:, :, i] = 1 / (1 + np.exp(-prediction_cpu[:, :, i]))
    grid = np.arange(grid_size)
    a, b = np.meshgrid(grid, grid)
    x_offset = a.reshape((-1, 1))
    y_offset = b.reshape((-1, 1))
    x_y_offset = np.concatenate((x_offset, y_offset), 1)
    x_y_offset = np.tile(x_y_offset, (1, num_anchors))
    x_y_offset = x_y_offset.reshape((-1, 2))
    x_y_offset = np.expand_dims(x_y_offset, 0)
    anchors = [(a[0] / stride, a[1] / stride) for a in anchors]
    anchors = np.tile(anchors, (grid_size * grid_size, 1))
    anchors = np.expand_dims(anchors, 0)
    prediction_cpu[:, :, :2] += x_y_offset
    prediction_cpu[:, :, 2:4] = np.exp(prediction_cpu[:, :, 2:4]) * anchors
    prediction_cpu[:, :, 5:5 + num_classes] = 1 / (1 + np.exp(-prediction_cpu[:, :, 5:5 + num_classes]))
    prediction_cpu[:, :, :4] *= stride
    return Tensor(prediction_cpu)