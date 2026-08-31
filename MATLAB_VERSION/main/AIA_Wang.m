function [Z, a, theta_hist] = AIA_Wang(aFull, maxIter, Tol)
    W = @(x) atan2(sin(x), cos(x));

    I = double(aFull);
    theta_hist = zeros(1, maxIter);

    [L, M, N] = size(I);
    P = L*M;

    theta = (2*pi/N) * (0:N-1)';

    X = reshape(I, P, N);

    for kIter = 1:maxIter
        theta_prev = theta;

        cosd = cos(theta);
        sind = sin(theta);

        A = zeros(3,3);
        A(1,1) = N;
        A(1,2) = sum(cosd);
        A(1,3) = sum(sind);

        A(2,1) = A(1,2);
        A(2,2) = sum(cosd.^2);
        A(2,3) = sum(cosd.*sind);

        A(3,1) = A(1,3);
        A(3,2) = A(2,3);
        A(3,3) = sum(sind.^2);

        Ainv = inv(A);

        S0 = X * ones(N,1);
        S1 = X * cosd;
        S2 = X * sind;

        Xj = Ainv * [S0.'; S1.'; S2.'];

        Axy = reshape(Xj(1,:), L, M);
        Uxy = reshape(Xj(2,:), L, M);
        Vxy = reshape(Xj(3,:), L, M);

        phi = atan2(-Vxy, Uxy);

        cosf = cos(phi(:));
        sinf = sin(phi(:));

        A2 = zeros(3,3);
        A2(1,1) = P;
        A2(1,2) = sum(cosf);
        A2(1,3) = sum(sinf);

        A2(2,1) = A2(1,2);
        A2(2,2) = sum(cosf.^2);
        A2(2,3) = sum(cosf.*sinf);

        A2(3,1) = A2(1,3);
        A2(3,2) = A2(2,3);
        A2(3,3) = sum(sinf.^2);

        A2Inv = inv(A2);

        T0 = sum(X, 1).';
        T1 = (cosf.' * X).';
        T2 = (sinf.' * X).';

        Xi = A2Inv * [T0.'; T1.'; T2.'];

        beta  = Xi(2,:).';
        gamma = Xi(3,:).';

        theta = atan2(-gamma, beta);

        err = norm((theta - theta(1)) - (theta_prev - theta_prev(1)));

        theta = W(theta - theta(1));
        theta_hist(kIter) = err;

        if err < Tol
            theta_hist = theta_hist(1:kIter);
            break;
        end
    end
    a = mat2gray(Axy);
    Z = Uxy - 1j*Vxy;

end
