%this file generates a density matrix of a squeezed state with amplitude
%alpha=x+ip and squeezing s*exp(i*theta) up to photon number=num_max
%this follows the notation in R. Loudon and P.L. Knight, Squeezed Light,
%Journal of Modern Optics, 34, 709 (1987). Equation 3.31. It uses
%HermitePoly, which can be found on the Matlab exchange
%by Jeff Lundeen 2008
Sn=@(n,x,p,s,theta) 1/sqrt(factorial(n)*cosh(s))*(exp(i*theta)*tanh(s)/2)^(n/2)...
    *exp(-(x^2+p^2+(x-i*p)*exp(i*theta)*tanh(s))/2)...
    *polyval(HermitePoly(n), (x+i*p+(x-i*p)*exp(i*theta)*tanh(s))/sqrt(2*exp(i*theta)*tanh(s)));
num_max=15;
x=1;
p=0;
s=0.5;
theta=0;
rho_mle=zeros(num_max+1,num_max+1);
for m=0:num_max
    for n=0:num_max
        rho_mle(m+1,n+1)=Sn(n,x,p,s,theta)*Sn(m,x,-p,s,-theta);
    end
end
save squeezedstate rho_mle