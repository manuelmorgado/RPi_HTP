%this file generates a density matrix of a schrodinger cat |alpha>+|-alpha> with amplitude
%alpha=x+ip up to photon number=num_max
num_max=15;
x=2;
p=0;
rho_mle=zeros(num_max+1,num_max+1);
for m=0:num_max
    for n=0:num_max
        rho_mle(m+1,n+1)=exp(-x^2-p^2)/realsqrt(factorial(m)*factorial(n))...
            *((x+i*p)^n*(x-i*p)^m+(-x-i*p)^n*(-x+i*p)^m...
            +(x+i*p)^n*(-x+i*p)^m+(-x-i*p)^n*(x-i*p)^m);
    end
end
save schrodinger rho_mle