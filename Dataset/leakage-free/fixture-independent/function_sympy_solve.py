from sympy import symbols, Eq, solve

def solve_quadratic_equation():
    x = symbols('x')
    
    equation = Eq(x**2 - 4, 0)
    
    solutions = solve(equation, x)
    
    return solutions
