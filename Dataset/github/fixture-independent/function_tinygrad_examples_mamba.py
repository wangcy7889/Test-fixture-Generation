from tinygrad import Tensor

def selective_scan_ref(u, delta, A, B, C, D=None, z=None, delta_bias=None, delta_softplus=False, return_last_state=False):
    u = u.float()
    delta = delta.float()
    if delta_bias is not None:
        delta = delta + delta_bias[..., None].float()
    if delta_softplus:
        delta = delta.softplus()
    batch, dim, dstate = (u.shape[0], A.shape[0], A.shape[1])
    is_variable_B = len(B.shape) >= 3
    is_variable_C = len(C.shape) >= 3
    x = Tensor.zeros(batch, dim, dstate)
    ys = []
    deltaA = Tensor.einsum('bdl,dn->bdln', delta, A).exp()
    if not is_variable_B:
        deltaB_u = Tensor.einsum('bdl,dn,bdl->bdln', delta, B, u)
    elif len(B.shape) == 3:
        deltaB_u = Tensor.einsum('bdl,bnl,bdl->bdln', delta, B, u)
    else:
        B = B.repeat((1, dim // B.shape[1], 1, 1))
        deltaB_u = Tensor.einsum('bdl,bdnl,bdl->bdln', delta, B, u)
    if is_variable_C and len(C.shape) == 4:
        C = C.repeat((1, dim // C.shape[1], 1, 1))
    last_state = None
    for i in range(u.shape[2]):
        x = deltaA[:, :, i] * x + deltaB_u[:, :, i]
        if not is_variable_C:
            y = Tensor.einsum('bdn,dn->bd', x, C)
        elif len(C.shape) == 3:
            y = Tensor.einsum('bdn,bn->bd', x, C[:, :, i])
        else:
            y = Tensor.einsum('bdn,bdn->bd', x, C[:, :, :, i])
        if i == u.shape[2] - 1:
            last_state = x
        ys.append(y)
    y = Tensor.stack(*ys, dim=2)
    out = y if D is None else y + u * D.reshape((-1, 1))
    if z is not None:
        out = out * z.silu()
    return out if not return_last_state else (out, last_state)