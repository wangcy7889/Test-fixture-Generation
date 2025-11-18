import numpy as np
import numdifftools as nd

def compute_hessian(func, x):
    
    if not isinstance(x, np.ndarray):
        raise ValueError("Input point x must be a NumPy array.")
    
    try:
        hessian_calculator = nd.Hessian(func)
        return hessian_calculator(x)
    except Exception as e:
        raise ValueError(f"Error in computing Hessian matrix: {e}")
