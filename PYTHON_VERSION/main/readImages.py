from pathlib import Path

import numpy as np
from PIL import Image

from utils import mat2gray


def readImages(path):
    files = sorted(Path(path).glob("*.png"))
    frames = []
    for file in files:
        image = np.array(Image.open(file))
        if image.ndim == 3:
            image = image[:, :, 0]
        frames.append(image)

    I_stack = np.stack(frames, axis=2)
    L, M, N = I_stack.shape
    I_stack = mat2gray(I_stack)
    return I_stack, L, M, N
