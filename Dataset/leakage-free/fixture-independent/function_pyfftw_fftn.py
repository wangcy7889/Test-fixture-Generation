import numpy as np
import pyfftw.interfaces
pyfftw.interfaces.cache.enable()

def compute_fftn(input_array):
    
    try:
        fftn_result = pyfftw.interfaces.numpy_fft.fftn(input_array)
        return fftn_result
    except Exception as e:
        return f"Error in computing FFTN: {e}"
