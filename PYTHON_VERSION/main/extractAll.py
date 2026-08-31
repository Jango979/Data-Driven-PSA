import numpy as np

from calculateEccentricity import calculateEccentricity
from utils import wrapToPi


def extractAll(Z, N):
    a = np.real(Z) / N
    a = (a - np.min(a)) / (np.max(a) - np.min(a))

    ZI = np.abs(Z)
    b = ZI / np.max(ZI)

    phi = wrapToPi(np.angle(Z))

    Liss, ecc = calculateEccentricity(np.real(Z), np.imag(Z))
    return a, b, phi, Liss, ecc
