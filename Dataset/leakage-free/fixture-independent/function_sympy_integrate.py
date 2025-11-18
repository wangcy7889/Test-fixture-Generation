from sympy import symbols, integrate, exp, sin, cos

def calculate_integral(expression_str, variable_str, lower_limit=None, upper_limit=None):
    x = symbols(variable_str)
    expression = eval(expression_str)
    
    if lower_limit is not None and upper_limit is not None:
        integral = integrate(expression, (x, lower_limit, upper_limit))
    else:
        integral = integrate(expression, x)
        
    return integral
