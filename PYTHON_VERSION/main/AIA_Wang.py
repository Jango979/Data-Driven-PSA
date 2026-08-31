import numpy as np

from utils import mat2gray, wrapToPi


def AIA_Wang(aFull, maxIter, Tol):
    I = np.asarray(aFull, dtype=float)
    L, M, N = I.shape
    P = L * M

    theta = (2 * np.pi / N) * np.arange(N)
    X = I.reshape(P, N)
    theta_hist = np.zeros(maxIter)

    Axy = np.zeros((L, M))
    Uxy = np.zeros((L, M))
    Vxy = np.zeros((L, M))

    for k in range(maxIter):
        theta_prev = theta.copy()
        cosd = np.cos(theta)
        sind = np.sin(theta)

        A = np.array(
            [
                [N, np.sum(cosd), np.sum(sind)],
                [np.sum(cosd), np.sum(cosd ** 2), np.sum(cosd * sind)],
                [np.sum(sind), np.sum(cosd * sind), np.sum(sind ** 2)],
            ]
        )
        Ainv = np.linalg.inv(A)

        S0 = X @ np.ones(N)
        S1 = X @ cosd
        S2 = X @ sind
        Xj = Ainv @ np.vstack((S0, S1, S2))

        Axy = Xj[0, :].reshape(L, M)
        Uxy = Xj[1, :].reshape(L, M)
        Vxy = Xj[2, :].reshape(L, M)

        phi = np.arctan2(-Vxy, Uxy)
        cosf = np.cos(phi.ravel())
        sinf = np.sin(phi.ravel())

        A2 = np.array(
            [
                [P, np.sum(cosf), np.sum(sinf)],
                [np.sum(cosf), np.sum(cosf ** 2), np.sum(cosf * sinf)],
                [np.sum(sinf), np.sum(cosf * sinf), np.sum(sinf ** 2)],
            ]
        )
        A2Inv = np.linalg.inv(A2)

        T0 = np.sum(X, axis=0)
        T1 = cosf @ X
        T2 = sinf @ X
        Xi = A2Inv @ np.vstack((T0, T1, T2))

        beta = Xi[1, :]
        gamma = Xi[2, :]
        theta = np.arctan2(-gamma, beta)

        err = np.linalg.norm((theta - theta[0]) - (theta_prev - theta_prev[0]))
        theta = wrapToPi(theta - theta[0])
        theta_hist[k] = err

        if err < Tol:
            theta_hist = theta_hist[: k + 1]
            break

    a = mat2gray(Axy)
    Z = Uxy - 1j * Vxy
    return Z, a, theta_hist
