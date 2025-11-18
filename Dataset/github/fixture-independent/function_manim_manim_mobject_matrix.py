from __future__ import annotations
import numpy as np

def matrix_to_tex_string(matrix):
    matrix = np.array(matrix).astype('str')
    if matrix.ndim == 1:
        matrix = matrix.reshape((matrix.size, 1))
    n_rows, n_cols = matrix.shape
    prefix = '\\left[ \\begin{array}{%s}' % ('c' * n_cols)
    suffix = '\\end{array} \\right]'
    rows = [' & '.join(row) for row in matrix]
    return prefix + ' \\\\ '.join(rows) + suffix