import numpy as np

def gaussian_kernel(n, std):
    from scipy import signal
    gaussian_1d = signal.windows.gaussian(n, std)
    gaussian_2d = np.outer(gaussian_1d, gaussian_1d)
    gaussian_3d = np.outer(gaussian_2d, gaussian_1d)
    gaussian_3d = gaussian_3d.reshape(n, n, n)
    gaussian_3d = np.cbrt(gaussian_3d)
    gaussian_3d /= gaussian_3d.max()
    return gaussian_3d