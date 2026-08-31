function [m_u_v,ecc] = calculateEccentricity(bcos, bsin)

x_c = (max(bcos(:)) + min(bcos(:))) / 2;
y_c = (max(bsin(:)) + min(bsin(:))) / 2;

c_g = [x_c, y_c];

u = bcos - c_g(1);
v = bsin - c_g(2);

r = sqrt(u.^2+v.^2);
[~,Ind_M] = max(r(:));


m_coeff= zeros(2,2);
m_coeff(1,1) = u(Ind_M); 
m_coeff(1,2) = v(Ind_M);
m_coeff(2,1) = m_coeff(1,2); 
m_coeff(2,2) = -m_coeff(1,1);

Inv_m = inv(m_coeff);

m_u_v = [u(:), v(:)] * Inv_m ;

rh = max(m_u_v(:,1))-min(m_u_v(:,1));
rv = max(m_u_v(:,2))-min(m_u_v(:,2));

a = max(rv,rh);
b = min(rv,rh);

ecc = sqrt(1-(b/a)^2);

end