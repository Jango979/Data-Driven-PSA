function [Z] = pca_func(I_stack)

    N = size(I_stack,3);
    I_p = double(I_stack);
    I_mean = mean(I_p,3);
    J = I_p - I_mean;
    X = reshape(J, [], N);
    C = X' * X;
    [matU,matS,~] = svds(C,2);

    coeff_u = matU(:,1) / sqrt(matS(1,1));
    coeff_v = matU(:,2) / sqrt(matS(2,2));
    U = tensorprod(J,coeff_u,3,1);
    V = tensorprod(J,coeff_v,3,1);
    Z = U + 1j*V;
end
