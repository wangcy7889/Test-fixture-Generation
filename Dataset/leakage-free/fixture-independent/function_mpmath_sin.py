import mpmath

def calculate_sin(x, precision=50):

    mpmath.mp.dps = precision 
    return str(mpmath.sin(x))
