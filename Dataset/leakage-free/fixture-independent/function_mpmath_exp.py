import mpmath

def calculate_exp(x, precision=50):
    
    mpmath.mp.dps = precision
    return str(mpmath.exp(x))
