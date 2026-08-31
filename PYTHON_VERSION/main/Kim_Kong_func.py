import numpy as np

from utils import mat2gray


def Kim_Kong_func(I, maxIter, Tol):
    I = np.asarray(I, dtype=float)
    a = mat2gray(I[:, :, 0])
    I_hat = I - I[:, :, [0]]
    Jxy = I_hat[:, :, 1:]
    L, M, N = Jxy.shape

    theta = 2 * np.pi / N * np.arange(N)
    beta = np.cos(theta) - 1
    gamma = -np.sin(theta)
    theta_hist = np.zeros(maxIter)

    Uxy = np.zeros((L, M))
    Vxy = np.zeros((L, M))

    for it in range(maxIter):
        A1 = np.column_stack((beta, gamma))
        pA1 = np.linalg.inv(A1.T @ A1) @ A1.T
        Uxy = np.tensordot(Jxy, pA1[0, :], axes=([2], [0]))
        Vxy = np.tensordot(Jxy, pA1[1, :], axes=([2], [0]))

        A2 = np.array(
            [
                [np.sum(Uxy * Uxy), np.sum(Uxy * Vxy)],
                [np.sum(Uxy * Vxy), np.sum(Vxy * Vxy)],
            ]
        )
        invA2 = np.linalg.inv(A2)
        theta_old = theta.copy()

        for n in range(N):
            tmp = Jxy[:, :, n]
            B = np.array([np.sum(tmp * Uxy), np.sum(tmp * Vxy)])
            X = invA2 @ B
            beta[n] = X[0]
            gamma[n] = X[1]

        theta = np.arctan2(-gamma, beta + 1)

        err = np.linalg.norm((theta - theta[0]) - (theta_old - theta_old[0]))
        theta_hist[it] = err
        beta = np.cos(theta) - 1
        gamma = -np.sin(theta)

        if err < Tol:
            break

    Z = Uxy + 1j * Vxy
    return Z, a, theta_hist
