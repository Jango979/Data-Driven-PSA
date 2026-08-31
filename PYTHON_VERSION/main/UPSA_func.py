import numpy as np

from utils import mat2gray


def UPSA_func(I_stack, version=None):
    def Vis(x):
        return 2 * mat2gray(x) - 1

    L, M, N = I_stack.shape
    w0 = 2 * np.pi / N
    n = np.arange(N)
    c = np.exp(-1j * w0 * n)

    Z0 = np.tensordot(I_stack, c, axes=([2], [0]))
    a = mat2gray(np.mean(I_stack, axis=2))

    u = Vis(np.real(Z0))
    v = Vis(np.imag(Z0))
    u2 = (u + v) / np.sqrt(2)
    v2 = (u - v) / np.sqrt(2)
    u3 = Vis(u2)
    v3 = Vis(v2)
    Z = u3 + 1j * v3
    return Z, a
