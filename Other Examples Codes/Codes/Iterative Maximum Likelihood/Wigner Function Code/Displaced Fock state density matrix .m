%this file generates a density matrix of a Fock state with photon number n displaced by amplitude
%alpha=x+ip up to a photon number=num_max
%This follows from the photon number representation of the displacement
%operator in Stephen Barnett's "Methods in Theoretical Quantum Optics". Eq. 4.4.46 It uses
%LaguerreGen.m, which can be found on the Matlab exchange
%by Jeff Lundeen 2008
num_max=20;
n=2;
x=1;
p=1;
rho_mle=zeros(num_max+1,num_max+1);
for k=0:num_max
    if k>=n
psi(k+1)=sqrt(factorial(n)/factorial(k))*exp(-(x^2)/2-(p^2)/2)*(x-i*p)^(k-n)*polyval(LaguerreGen(n,k-n),x^2+p^2);
    else
psi(k+1)=sqrt(factorial(k)/factorial(n))*exp(-(x^2)/2-(p^2)/2)*(-x-i*p)^(n-k)*polyval(LaguerreGen(k,n-k),x^2+p^2);        
    end  
end
rho_mle=psi'*psi;
save displacedfock rho_mle