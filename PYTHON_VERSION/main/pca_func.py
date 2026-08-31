import numpy as np


def pca_func(I_stack):
    N = I_stack.shape[2]
    I_p = np.asarray(I_stack, dtype=float)
    I_mean = np.mean(I_p, axis=2, keepdims=True)
    J = I_p - I_mean
    X = J.reshape(-1, N)
    C = X.T @ X

    eigvals, eigvecs = np.linalg.eigh(C)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    coeff_u = eigvecs[:, 0] / np.sqrt(eigvals[0])
    coeff_v = eigvecs[:, 1] / np.sqrt(eigvals[1])
    U = np.tensordot(J, coeff_u, axes=([2], [0]))
    V = np.tensordot(J, coeff_v, axes=([2], [0]))
    Z = U + 1j * V
    return Z
