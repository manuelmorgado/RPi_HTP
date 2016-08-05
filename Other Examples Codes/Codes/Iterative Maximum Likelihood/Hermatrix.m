function Hermatrix=Hermatrix(n_max)
%This generates a matrix of the Hermite Polynomial coefficients for all
%polynomials up to order n_max
%Hermatrix[i,n_max+1-k]=the kth coefficient of the ith polynomial
Hermatrix=zeros(n_max+1,n_max+1);
for j=0:n_max
    Hermatrix(j+1,n_max-j+1:n_max+1)=HermitePoly(j);
end;
Hermatrix=Hermatrix';

