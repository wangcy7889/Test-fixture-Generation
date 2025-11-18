from decimal import Decimal

def get_decimal_adjusted(value):
    
    decimal_value = Decimal(str(value))

    if decimal_value == 0:
        return Decimal('-Infinity')
    
    return decimal_value.adjusted()
