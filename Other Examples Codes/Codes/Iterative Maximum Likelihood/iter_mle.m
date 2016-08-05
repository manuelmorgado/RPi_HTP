function [rho_mle,loglik]=iter_mle(POVM,iter)
%Based on: A.I. Lvovsky, "Iterative maximum-likelihood reconstruction in quantum homodyne tomography" J. Opt. B: Quantum Semiclass. Opt. 6 (2004) S556–S559
%By Jeff Lundeen, 2008
%normalization [x,p]=i/2 is used
%This code does maximum likelihood estimation of an unknown state using
%balanced homodyne tomographic data
%Input:
%POVM(n,m,j) is the n,m element of the meaurement operator of the jth data point, in the fock basis. Generate this with tomoset.m
%iter is the number of desired iterations, 20 is more than enough.
%Output:
%rho_mle is the estimated state in the fock basis
%loglik is a vector of the log likelihood functions calculated in the iterations

%number of data points
num_data=size(POVM,3);
%nrho-1 is the maximum photon number in the reconstructed state
nrho=size(POVM,2);
%initialize the first guess as the identity, properly normalized
rho_mle=eye(nrho)/nrho;
%initialize matrix
Y=zeros(nrho,nrho,num_data);
for j=1:iter
    %update rho
    rho = rho_mle;
    Y=rho(:,:,ones(1,num_data));
    %calculate Tr(POVM(i)*rho) for all i
    trR = squeeze(real((sum(sum(conj(POVM).*Y,1),2))));
    Y = permute(trR(:,ones(1,nrho),ones(1,nrho)),[2,3,1]);
    %calculate R from the Lvovsky paper
    R = sum(POVM./Y,3);
    %Update rho_mle, this increases the log likelihood and ensures positivity since R is Hermitian
    rho_mle = (R*rho*R);
    %Normalize rho
    rho_mle = rho_mle/sum(diag(rho_mle));
    %Calculate log likelihood to plot later
    loglik(j)=sum(log(trR));
end;
    
    
