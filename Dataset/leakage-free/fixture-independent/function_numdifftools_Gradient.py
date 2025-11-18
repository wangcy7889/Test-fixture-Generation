import numpy as np
import numdifftools as nd

def analyze_gradient(func, x, mode="compute", tol=1e-6):
   
    if not isinstance(x, np.ndarray):
        raise ValueError("Input point x must be a NumPy array.")
    
    try:
        gradient_calculator = nd.Gradient(func)
        gradient = gradient_calculator(x)
    except Exception as e:
        raise ValueError(f"Error in computing gradient: {e}")
    
    if mode == "compute":
        return gradient
    elif mode == "norm":
        return np.linalg.norm(gradient)
    elif mode == "unit":
        norm = np.linalg.norm(gradient)
        return gradient / norm if norm != 0 else np.zeros_like(gradient)
    elif mode == "direction":
        return np.sign(gradient)
    elif mode == "zero_check":
        return np.all(np.abs(gradient) < tol)
    else:
        raise ValueError(f"Invalid mode: {mode}")
