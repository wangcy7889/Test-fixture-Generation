import numpy as np

def solve_linear_system(matrix: np.ndarray) -> np.ndarray:
    ab = np.copy(matrix)
    num_of_rows = ab.shape[0]
    num_of_columns = ab.shape[1] - 1
    x_lst: list[float] = []
    if num_of_rows != num_of_columns:
        raise ValueError('Matrix is not square')
    for column_num in range(num_of_rows):
        for i in range(column_num, num_of_columns):
            if abs(ab[i][column_num]) > abs(ab[column_num][column_num]):
                ab[[column_num, i]] = ab[[i, column_num]]
        if abs(ab[column_num, column_num]) < 1e-08:
            raise ValueError('Matrix is singular')
        if column_num != 0:
            for i in range(column_num, num_of_rows):
                ab[i, :] -= ab[i, column_num - 1] / ab[column_num - 1, column_num - 1] * ab[column_num - 1, :]
    for column_num in range(num_of_rows - 1, -1, -1):
        x = ab[column_num, -1] / ab[column_num, column_num]
        x_lst.insert(0, x)
        for i in range(column_num - 1, -1, -1):
            ab[i, -1] -= ab[i, column_num] * x
    return np.asarray(x_lst)