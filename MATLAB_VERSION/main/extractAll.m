function [a,b,phi,Liss,ecc] = extractAll(Z,N)

t = linspace(0,2*pi,400); 
a = real(Z)/N;
a = (a - min(a(:))) ./ (max(a(:)) - min(a(:)));


ZI = abs(Z);
b = ZI / max(ZI(:));

phi = wrapToPi(angle(Z));

[Liss, ecc] = calculateEccentricity(real(Z), imag(Z));
end