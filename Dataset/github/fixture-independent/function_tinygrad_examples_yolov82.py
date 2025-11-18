from tinygrad.tensor import Tensor

def make_anchors(feats, strides, grid_cell_offset=0.5):
    anchor_points, stride_tensor = ([], [])
    assert feats is not None
    for i, stride in enumerate(strides):
        _, _, h, w = feats[i].shape
        sx = Tensor.arange(w) + grid_cell_offset
        sy = Tensor.arange(h) + grid_cell_offset
        sx = sx.reshape(1, -1).repeat([h, 1]).reshape(-1)
        sy = sy.reshape(-1, 1).repeat([1, w]).reshape(-1)
        anchor_points.append(Tensor.stack(sx, sy, dim=-1).reshape(-1, 2))
        stride_tensor.append(Tensor.full(h * w, stride))
    anchor_points = anchor_points[0].cat(anchor_points[1], anchor_points[2])
    stride_tensor = stride_tensor[0].cat(stride_tensor[1], stride_tensor[2]).unsqueeze(1)
    return (anchor_points, stride_tensor)