from patsy.desc import ModelDesc
import unittest

def parse_formula(formula):
    
    if not isinstance(formula, str):
        raise TypeError("Formula must be a string.")
    try:
        model_desc = ModelDesc.from_formula(formula)
    except Exception as e:
        raise ValueError(f"Failed to parse formula: {e}")
    return model_desc
