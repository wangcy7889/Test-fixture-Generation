from decimal import Decimal

def get_decimal_tuple(value):
    
    decimal_value = Decimal(str(value))
    
    return decimal_value.as_tuple()
