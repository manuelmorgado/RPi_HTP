%This code tests the mle program by generating fake data, X, generating the
%corresponding set of measurement operators, T, and then doing an iterative
%maximum likelihood procedure to find rho_mle, the estimated state, which is saves in file "results".
%Run Wigner.m to plot the Wigner function of the state
X=Fock_zero(10000);
T=tomoset(X, 0.9999, 10);
[rho_mle, loglik]=iter_mle(T,20);
real(rho_mle(1:5,1:5))
plot(diag(real(rho_mle)))
save results rho_mle