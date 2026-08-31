import numpy as np

from utils import mat2gray


def bruning_func(I):
    I = np.asarray(I, dtype=float)
    N = I.shape[2]
    w0 = 2 * np.pi / N
    n = np.arange(N)
    c = np.exp(-1j * w0 * n)

    Z = np.tensordot(I, c, axes=([2], [0]))
    a = mat2gray(np.mean(I, axis=2))
    return Z, a
