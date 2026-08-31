import numpy as np


def calculateEccentricity(bcos, bsin):
    x_c = (np.max(bcos) + np.min(bcos)) / 2
    y_c = (np.max(bsin) + np.min(bsin)) / 2

    u = bcos - x_c
    v = bsin - y_c

    r = np.sqrt(u ** 2 + v ** 2)
    u_flat = u.ravel()
    v_flat = v.ravel()
    ind_m = np.argmax(r.ravel())

    m_coeff = np.array(
        [
            [u_flat[ind_m], v_flat[ind_m]],
            [v_flat[ind_m], -u_flat[ind_m]],
        ]
    )
    inv_m = np.linalg.inv(m_coeff)

    m_u_v = np.column_stack((u_flat, v_flat)) @ inv_m

    rh = np.max(m_u_v[:, 0]) - np.min(m_u_v[:, 0])
    rv = np.max(m_u_v[:, 1]) - np.min(m_u_v[:, 1])

    a = max(rv, rh)
    b = min(rv, rh)
    ecc = np.sqrt(1 - (b / a) ** 2)
    return m_u_v, ecc
