import re
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from AIA_Wang import AIA_Wang
from bruning_func import bruning_func
from fourPlots import fourPlots
from Kim_Kong_func import Kim_Kong_func
from pca_func import pca_func
from trimWhiteRegions import trimWhiteRegions
from UPSA_func import UPSA_func
from utils import mat2gray

BASE_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = BASE_DIR.parent / "Samples" / "FPP"

files = sorted(
    SAMPLES_DIR.glob("synth*.png"),
    key=lambda p: int(re.search(r"\d+", p.stem).group()),
)

selectedIndices = [0, 7, 17, 20, 26]
files = [files[i] for i in selectedIndices]

frames = []
for file in files:
    image = np.array(Image.open(file))
    if image.ndim == 3:
        image = image[:, :, 0]
    frames.append(image)

Ixy = np.stack(frames, axis=2)
Ixy = mat2gray(Ixy)

Tol = 1e-4
maxIter = 60

t0 = time.time()
Z_B, a_B = bruning_func(Ixy)
print(time.time() - t0)

t0 = time.time()
Z_KK, a_KK, _ = Kim_Kong_func(Ixy, maxIter, Tol)
print(time.time() - t0)

t0 = time.time()
Z_AIA, a_AIA, _ = AIA_Wang(Ixy, maxIter, Tol)
print(time.time() - t0)

t0 = time.time()
Z_PCA = pca_func(Ixy)
print(time.time() - t0)
a_PCA = mat2gray(np.mean(Ixy, axis=2))

t0 = time.time()
Z_UPSA, a_UPSA = UPSA_func(Ixy)
print(time.time() - t0)

fig = plt.figure(figsize=(16, 10), facecolor="white")
gs = fig.add_gridspec(6, 5, wspace=0.15, hspace=0.15)

rows_data = [
    (a_B, Z_B, "Bruning"),
    (a_KK, Z_KK, "K&K"),
    (a_AIA, Z_AIA, "AIA"),
    (a_PCA, np.conj(Z_PCA), "PCA"),
    (a_UPSA, np.conj(Z_UPSA), "UPSA"),
]

a_ref = None
for k, (a, Z, name) in enumerate(rows_data):
    axes_row = [fig.add_subplot(gs[k, c]) for c in range(5)]
    a_ref = fourPlots(axes_row, a, Z, name, show_titles=(k == 0))

ax_cb_a = fig.add_subplot(gs[5, 1])
ax_cb_a.imshow(np.ones_like(a_ref), cmap="gray", vmin=0, vmax=1)
ax_cb_a.axis("off")
fig.colorbar(ax_cb_a.images[0], ax=ax_cb_a, orientation="horizontal", fraction=0.5)

ax_cb_b = fig.add_subplot(gs[5, 2])
ax_cb_b.imshow(np.ones_like(a_ref), cmap="gray", vmin=0, vmax=1)
ax_cb_b.axis("off")
fig.colorbar(ax_cb_b.images[0], ax=ax_cb_b, orientation="horizontal", fraction=0.5)

ax_cb_phi = fig.add_subplot(gs[5, 3])
ax_cb_phi.imshow(np.pi * np.ones_like(a_ref), cmap="gray", vmin=-np.pi, vmax=np.pi)
ax_cb_phi.axis("off")
cb_phi = fig.colorbar(ax_cb_phi.images[0], ax=ax_cb_phi, orientation="horizontal", fraction=0.5)
cb_phi.set_ticks([-3, 0, 3])
cb_phi.set_ticklabels(["-3", "0", "3"])

ax_legend = fig.add_subplot(gs[5, 4])
ax_legend.imshow(np.ones_like(a_ref), cmap="gray", vmin=0, vmax=1)
ax_legend.axis("off")
ax_legend.text(0.5, 0.5, "-- Unit circle", ha="center", va="center", transform=ax_legend.transAxes)

fig.savefig(BASE_DIR / "Test.png", dpi=300)
trimWhiteRegions(BASE_DIR / "Test.png", BASE_DIR / "Trimmed.png", 255, 5)

plt.show()
