from mpmath import mp

def calculate_log(x: float, base: float = 10, precision: int = 50) -> str:
    
    mp.dps = precision
    
    if x <= 0:
        return "undefined" 
    return str(mp.log(x, base))
