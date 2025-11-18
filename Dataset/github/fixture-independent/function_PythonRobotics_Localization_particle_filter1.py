import numpy as np

def calc_covariance(x_est, px, pw):
    cov = np.zeros((4, 4))
    n_particle = px.shape[1]
    for i in range(n_particle):
        dx = px[:, i:i + 1] - x_est
        cov += pw[0, i] * dx @ dx.T
    cov *= 1.0 / (1.0 - pw @ pw.T)
    return cov