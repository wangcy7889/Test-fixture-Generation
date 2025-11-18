from decimal import Decimal, ROUND_HALF_UP

def set_decimal_precision(value, precision):
    
    decimal_value = Decimal(str(value))
    
    target_precision = Decimal('1e-{0}'.format(precision))
    
    return decimal_value.quantize(target_precision, rounding=ROUND_HALF_UP)
