function tomoset=tomoset(data,eta,num_max)
%Based on: A.I. Lvovsky, "Iterative maximum-likelihood reconstruction in quantum homodyne tomography" J. Opt. B: Quantum Semiclass. Opt. 6 (2004) S556–S559
%By Jeff Lundeen, 2008
%normalization [x,p]=i/2 is used
%
%This function calculates the Homodyne POVM matrices in the fock basis corresponding to every
%data point. The set is used in the iterative maximum likelihood routine,
%iter_mle.m. It expects a data set of form: data(j,1)=x(j) (i.e. the difference signal) and
%data(j,2)=theta(j) (i.e. the phase of the local oscillator). It also needs the efficiency
%of the Homodyne detector, eta, and the truncation photon number, num_max,
%which sets the size of the POVM matrices.
%
%It returns a matrix, tomoset. tomoset(n,m,j) is the n,m element of the
%meaurement operator of the jth data point.
%
%With eta not equal to 1, truncation should be past photon number
%num_max=ln(e)/ln(1-eta), where e is the fractional error in the highest phot. num elements of the POVM matrix 

[M,N,K]=ndgrid(1:num_max+1,1:num_max+1,1:num_max+1);
%initialize matrices
tomoset=zeros(num_max+1,num_max+1,size(data,1));
s=zeros(num_max+1,num_max+1);
%Precalculate Hermite polynomials
Hmatrix=Hermatrix(num_max);
mult=(num_max:-1:0)';
tic
for j=1:size(data,1)
    j
    %Calculate H_n(sqrt(x)), where H_n is the nth Hermite polynomial
    Herm=(1.4142135*data(j,1)).^mult;
    H_n=Herm(:,ones(1,num_max+1));
    H_n=Hmatrix.*H_n;
    H_nx=sum(H_n,1);
    %Calculate POVM matrix for jth data point
    s=loss(M-1,K-1,eta).*loss(N-1,K-1,eta).*HO(N-K,data(j,1),data(j,2))...
        .*HO(M-K,data(j,1),-data(j,2)).*H_nx(abs(M-K)+1)...
        .*H_nx(abs(N-K)+1);
    tomoset(:,:,j)=sum(s,3);
end;
toc
end