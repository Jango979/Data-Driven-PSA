import numpy as np


def mat2gray(x):
    x = np.asarray(x, dtype=float)
    xmin = x.min()
    xmax = x.max()
    if xmax == xmin:
        return np.zeros_like(x)
    return (x - xmin) / (xmax - xmin)


def wrapToPi(x):
    return np.mod(x + np.pi, 2 * np.pi) - np.pi
