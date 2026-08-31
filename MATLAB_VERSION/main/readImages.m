function [I_stack,L,M,N] = readImages(path)
    imagenDir = dir(fullfile(path, '*.png'));
    I_stack = [];
    
    for k = 1:numel(imagenDir)
        I = imread(fullfile(path, imagenDir(k).name));
        if ndims(I) == 3
            I = I(:,:,1);
        end
        I_stack(:,:,k) = I;
    
    end
    
    [L,M,N] = size(I_stack);
    I_stack = mat2gray(I_stack);

end