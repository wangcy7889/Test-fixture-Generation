import math
import numpy as np

def circle_fitting(x, y):
    sumx = sum(x)
    sumy = sum(y)
    sumx2 = sum([ix ** 2 for ix in x])
    sumy2 = sum([iy ** 2 for iy in y])
    sumxy = sum([ix * iy for ix, iy in zip(x, y)])
    F = np.array([[sumx2, sumxy, sumx], [sumxy, sumy2, sumy], [sumx, sumy, len(x)]])
    G = np.array([[-sum([ix ** 3 + ix * iy ** 2 for ix, iy in zip(x, y)])], [-sum([ix ** 2 * iy + iy ** 3 for ix, iy in zip(x, y)])], [-sum([ix ** 2 + iy ** 2 for ix, iy in zip(x, y)])]])
    T = np.linalg.inv(F).dot(G)
    cxe = float(T[0, 0] / -2)
    cye = float(T[1, 0] / -2)
    re = math.sqrt(cxe ** 2 + cye ** 2 - T[2, 0])
    error = sum([np.hypot(cxe - ix, cye - iy) - re for ix, iy in zip(x, y)])
    return (cxe, cye, re, error)