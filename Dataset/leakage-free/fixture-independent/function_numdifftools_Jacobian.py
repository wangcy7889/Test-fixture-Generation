import numpy as np
import numdifftools as nd

def compute_jacobian(func, x):
    
    try:
        if not callable(func):
            raise ValueError("The input 'func' must be callable.")
        if not isinstance(x, (np.ndarray, list)):
            raise ValueError("The input 'x' must be a NumPy array or a list.")
        
        # Compute the Jacobian using numdifftools.Jacobian
        jacobian_func = nd.Jacobian(func)
        return jacobian_func(x)
    except Exception as e:
        raise ValueError(f"Error in computing Jacobian: {e}")
