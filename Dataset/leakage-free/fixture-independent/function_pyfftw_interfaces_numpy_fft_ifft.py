import pyfftw
import numpy as np

def compute_ifft(input_array):

    try:
        if not np.issubdtype(input_array.dtype, np.complexfloating):
            raise ValueError("Input array must contain complex numbers.")
        return pyfftw.interfaces.numpy_fft.ifft(input_array)
    except Exception as e:
        raise ValueError(f"Error in computing IFFT: {e}")
