function [Z, a, theta_hist] = Kim_Kong_func(I, maxIter, Tol)
    I = double(I);
    a = mat2gray(I(:,:,1));
    I_hat = I - I(:,:,1);
    Jxy  = I_hat(:,:,2:end);
    [L,M,N] = size(Jxy);
    theta = 2*pi/N*(0:N-1)';
    beta  = cos(theta) - 1;
    gamma = -sin(theta);
    theta_hist = zeros(1, maxIter);

    for iter = 1:maxIter
        A1  = zeros(N,2);
        A1(:,1) = beta;
        A1(:,2) = gamma;
        pA1 = inv(A1' * A1) * A1';
        Uxy = tensorprod(Jxy, pA1(1,:), 3, 2);
        Vxy = tensorprod(Jxy, pA1(2,:), 3, 2);
        A2 = zeros(2,2);
        A2(1,1) = sum(sum(Uxy.*Uxy));
        A2(1,2) = sum(sum(Uxy.*Vxy));
        A2(2,1) = A2(1,2);
        A2(2,2) = sum(sum(Vxy.*Vxy));
        invA2 = inv(A2);
        theta_old = theta;

        for n = 1:N
            tmp = Jxy(:,:,n);
            B = zeros(2,1);
            B(1) = sum(sum(tmp.*Uxy));
            B(2) = sum(sum(tmp.*Vxy));
            X = invA2 * B;
            beta(n)  = X(1);
            gamma(n) = X(2);
        end

        theta = atan2(-gamma, beta + 1);

        err = norm((theta - theta(1)) - (theta_old - theta_old(1)));
        theta_hist(iter) = err;
        beta  = cos(theta) - 1;
        gamma = -sin(theta);

        if err < Tol
            %theta_hist = theta_hist(1:iter);
            break;
        end
    end

    Z = complex(Uxy, Vxy);
end