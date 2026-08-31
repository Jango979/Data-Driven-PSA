function trimWhiteRegions(inputFile, outputFile, threshold, thinWidth)
    if nargin < 3, threshold = 240; end
    if nargin < 4, thinWidth = 1;   end

    img = imread(inputFile);
    if size(img, 3) == 3
        img = rgb2gray(img);
    end
    img = double(img);

    colIsWhite = all(img >= threshold, 1);
    newCols    = selectIndices(colIsWhite, thinWidth);

    rowIsWhite = all(img >= threshold, 2);
    newRows    = selectIndices(rowIsWhite', thinWidth);

    imgOut = img(newRows, newCols);

    imwrite(uint8(imgOut), outputFile);
    fprintf('Saved trimmed image (%d×%d) to "%s"\n', ...
            size(imgOut,1), size(imgOut,2), outputFile);
end


function keepIdx = selectIndices(isWhite, thinWidth)
    N       = numel(isWhite);
    keepIdx = false(1, N);
    i       = 1;

    while i <= N
        if ~isWhite(i)
            keepIdx(i) = true;
            i = i + 1;
        else
            j = i;
            while j <= N && isWhite(j)
                j = j + 1;
            end
            runLen = j - i;

            kept = round(linspace(i, j-1, min(thinWidth, runLen)));
            keepIdx(kept) = true;
            i = j;
        end
    end

    keepIdx = find(keepIdx);
end
