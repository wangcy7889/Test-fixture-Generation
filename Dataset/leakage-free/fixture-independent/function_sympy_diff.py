from sympy import symbols, diff, sin, exp


def calculate_derivative(expression_str, variable_str, order=1):
    x = symbols(variable_str)
    expression = eval(expression_str)
    derivative = diff(expression, x, order)
    return derivative
