function [Z,a] = UPSA_func(I_stack,version)
    Vis = @(x) (2*mat2gray(x))-1;
    [L, M, N] = size(I_stack);
    w0 = 2*pi/N;
    n = 0:N-1;
    c = exp(-1j*w0*n);
    
    Z0 = tensorprod(I_stack, c, 3, 2);
    a = mat2gray(mean(I_stack, 3));                          
    u = Vis(real(Z0)); v = Vis(imag(Z0));
    u2 = (u+v)/sqrt(2); v2 = (u-v)/sqrt(2);
    u3 = Vis(u2); v3 = Vis(v2);
    Z = u3 + 1j*v3;

end