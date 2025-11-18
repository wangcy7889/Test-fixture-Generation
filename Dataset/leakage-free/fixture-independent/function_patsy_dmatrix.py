from patsy.highlevel import dmatrix


def create_design_matrix(data=None, formula=None):
    if data is None or formula is None:
        raise ValueError("Error: data and formula are required")

    result = dmatrix(formula, data)
    return True, result

