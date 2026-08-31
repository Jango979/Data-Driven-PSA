import numpy as np

from calculateEccentricity import calculateEccentricity
from utils import wrapToPi


def fourPlots(axes_row, a, Z, name, show_titles):
    ax_label, ax_a, ax_b, ax_phi, ax_liss = axes_row

    Z = Z / np.max(np.abs(Z))
    u = np.real(Z).ravel()
    v = np.imag(Z).ravel()
    PhiW = np.angle(Z)
    PhiW = wrapToPi(PhiW - PhiW[0, 0])
    q = np.linspace(-np.pi, np.pi, 512)

    _, ecc = calculateEccentricity(np.real(Z), np.imag(Z))
    ax_label.text(0.8, 0.5, f"{name},\n ecc={ecc:.4f}", ha="center", va="center")
    ax_label.axis("off")

    a_norm = a / np.max(a)

    for ax, img, vmin, vmax in (
        (ax_a, a_norm, 0, 1),
        (ax_b, np.abs(Z), 0, 1),
        (ax_phi, PhiW, -np.pi, np.pi),
    ):
        ax.imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor("black")
            spine.set_linewidth(0.5)

    if show_titles:
        ax_a.set_title("$a$")
        ax_b.set_title("$b$")
        ax_phi.set_title(r"$\varphi$")

    ax_liss.scatter(u, v, color=(0.67, 0.67, 0.67))
    ax_liss.plot(np.cos(q), np.sin(q), "--k", linewidth=1)
    ax_liss.set_xlim(-1.1, 1.1)
    ax_liss.set_ylim(-1.1, 1.1)
    ax_liss.set_aspect("equal")
    ax_liss.set_xticks([-1, 0, 1])
    ax_liss.set_yticks([-1, 0, 1])
    ax_liss.set_xticklabels([])
    ax_liss.set_yticklabels([])
    ax_liss.spines["left"].set_position("zero")
    ax_liss.spines["bottom"].set_position("zero")
    ax_liss.spines["right"].set_color("none")
    ax_liss.spines["top"].set_color("none")
    ax_liss.grid(True, which="both", linestyle=":", linewidth=0.5)
    if show_titles:
        ax_liss.set_title("Lissajous")

    return a_norm
