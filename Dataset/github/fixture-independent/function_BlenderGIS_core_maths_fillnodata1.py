import numpy as np
DTYPEf = np.float32

def replace_nans(array, max_iter, tolerance, kernel_size=1, method='localmean'):
    filled = np.empty([array.shape[0], array.shape[1]], dtype=DTYPEf)
    kernel = np.empty((2 * kernel_size + 1, 2 * kernel_size + 1), dtype=DTYPEf)
    inans, jnans = np.nonzero(np.isnan(array))
    n_nans = len(inans)
    replaced_new = np.zeros(n_nans, dtype=DTYPEf)
    replaced_old = np.zeros(n_nans, dtype=DTYPEf)
    if method == 'localmean':
        for i in range(2 * kernel_size + 1):
            for j in range(2 * kernel_size + 1):
                kernel[i, j] = 1
    elif method == 'idw':
        kernel = np.array([[0, 0.5, 0.5, 0.5, 0], [0.5, 0.75, 0.75, 0.75, 0.5], [0.5, 0.75, 1, 0.75, 0.5], [0.5, 0.75, 0.75, 0.5, 1], [0, 0.5, 0.5, 0.5, 0]])
    else:
        raise ValueError("method not valid. Should be one of 'localmean', 'idw'.")
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            filled[i, j] = array[i, j]
    for it in range(max_iter):
        for k in range(n_nans):
            i = inans[k]
            j = jnans[k]
            filled[i, j] = 0.0
            n = 0
            for I in range(2 * kernel_size + 1):
                for J in range(2 * kernel_size + 1):
                    if i + I - kernel_size < array.shape[0] and i + I - kernel_size >= 0:
                        if j + J - kernel_size < array.shape[1] and j + J - kernel_size >= 0:
                            if filled[i + I - kernel_size, j + J - kernel_size] == filled[i + I - kernel_size, j + J - kernel_size]:
                                if I - kernel_size != 0 and J - kernel_size != 0:
                                    filled[i, j] = filled[i, j] + filled[i + I - kernel_size, j + J - kernel_size] * kernel[I, J]
                                    n = n + 1 * kernel[I, J]
            if n != 0:
                filled[i, j] = filled[i, j] / n
                replaced_new[k] = filled[i, j]
            else:
                filled[i, j] = np.nan
        if np.mean((replaced_new - replaced_old) ** 2) < tolerance:
            break
        else:
            for l in range(n_nans):
                replaced_old[l] = replaced_new[l]
    return filled