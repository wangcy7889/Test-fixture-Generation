import numpy as np
DTYPEf = np.float32

def sincinterp(image, x, y, kernel_size=3):
    r = np.zeros([x.shape[0], x.shape[1]], dtype=DTYPEf)
    pi = 3.1419
    for I in range(x.shape[0]):
        for J in range(x.shape[1]):
            for i in range(int(x[I, J]) - kernel_size, int(x[I, J]) + kernel_size + 1):
                for j in range(int(y[I, J]) - kernel_size, int(y[I, J]) + kernel_size + 1):
                    if i >= 0 and i <= image.shape[0] and (j >= 0) and (j <= image.shape[1]):
                        if i - x[I, J] == 0.0 and j - y[I, J] == 0.0:
                            r[I, J] = r[I, J] + image[i, j]
                        elif i - x[I, J] == 0.0:
                            r[I, J] = r[I, J] + image[i, j] * np.sin(pi * (j - y[I, J])) / (pi * (j - y[I, J]))
                        elif j - y[I, J] == 0.0:
                            r[I, J] = r[I, J] + image[i, j] * np.sin(pi * (i - x[I, J])) / (pi * (i - x[I, J]))
                        else:
                            r[I, J] = r[I, J] + image[i, j] * np.sin(pi * (i - x[I, J])) * np.sin(pi * (j - y[I, J])) / (pi * pi * (i - x[I, J]) * (j - y[I, J]))
    return r