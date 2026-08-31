import numpy as np
from PIL import Image


def _select_indices(is_white, thin_width):
    n = len(is_white)
    keep = np.zeros(n, dtype=bool)
    i = 0
    while i < n:
        if not is_white[i]:
            keep[i] = True
            i += 1
        else:
            j = i
            while j < n and is_white[j]:
                j += 1
            run_len = j - i
            k = min(thin_width, run_len)
            kept = np.round(np.linspace(i, j - 1, k)).astype(int)
            keep[kept] = True
            i = j
    return np.where(keep)[0]


def trimWhiteRegions(inputFile, outputFile, threshold=240, thinWidth=1):
    img = np.array(Image.open(inputFile).convert("L")).astype(float)

    colIsWhite = np.all(img >= threshold, axis=0)
    newCols = _select_indices(colIsWhite, thinWidth)

    rowIsWhite = np.all(img >= threshold, axis=1)
    newRows = _select_indices(rowIsWhite, thinWidth)

    imgOut = img[np.ix_(newRows, newCols)]
    Image.fromarray(imgOut.astype(np.uint8)).save(outputFile)
    print(f'Saved trimmed image ({imgOut.shape[0]}x{imgOut.shape[1]}) to "{outputFile}"')
