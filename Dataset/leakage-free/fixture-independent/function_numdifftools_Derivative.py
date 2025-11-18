import numdifftools as nd

def compute_derivative(func, x, order=1):
    
    if not isinstance(order, int) or order < 1:
        raise ValueError("Order must be a positive integer.")
    
    try:
        derivative = nd.Derivative(func, n=order)
        return derivative(x)
    except Exception as e:
        raise ValueError(f"Error in computing derivative: {e}")
