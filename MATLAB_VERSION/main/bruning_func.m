function [Z,a] = bruning_func(I)
    I = double(I);

    [~, ~, N] = size(I);

    w0 = 2*pi/N;
    n = 0:N-1;                      
    c = exp(-1j*w0*n);              

         
    Z = tensorprod(I,c,3,2);

    a = mat2gray(mean(I, 3));

end
