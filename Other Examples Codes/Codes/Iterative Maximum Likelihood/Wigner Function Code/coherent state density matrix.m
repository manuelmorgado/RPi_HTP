%this file generates a density matrix of a squeezed state with amplitude
%alpha=x+ip and squeezing s*exp(i*theta) up to photon number=num_max
%this follows the notation in R. Loudon and P.L. Knight, Squeezed Light,
%Journal of Modern Optics, 34, 709 (1987). Equation 3.31
num_max=15;
x=1;
p=1;
rho_mle=zeros(num_max+1,num_max+1);
sqrt(factorial(n)*cosh(s))*(exp(i*theta)
for m=0:num_max
    for n=0:num_max
        rho_mle(m+1,n+1)=exp(-x^2-p^2)*(x+i*p)^n*(x-i*p)^m/realsqrt(factorial(m)*factorial(n));
    end
end
save coherent rho_mle