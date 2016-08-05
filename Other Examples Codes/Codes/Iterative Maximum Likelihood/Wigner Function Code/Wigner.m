
% Wigner.m
% By Jeff Lundeen, 2008
% This is based on a similar programs by Alvaro Feito and Graciana Puentes

% Given:
%   1. A density matrix saved in a file: results.m with the name rho_mle
%   2. The range of the phase space plot
% Return a 3d plot of the Wigner function

clear all;


%% load the density matrix %%
load displacedfock
%test matrix: a three photon fock state
%rho_mle=zeros(5,5);
%rho_mle(4,4)=1;
%% The maximum photon number in the density matrix
num_max=size(rho_mle,1)-1;
%% chose range %%
x_max=5;
x_min=-5;
p_max=5;
p_min=-5;

%% choose the number of points across each axis %%
numpoint=25;
x=x_min:((x_max-x_min)/numpoint):x_max;
p=p_min:((p_max-p_min)/numpoint):p_max;
%
%% Generate the Wigner function %%

%If there is enough memory (e.g. > 1GB), vectorize K by k->K ,remove the
%for loop, and uncomment the following line:
%[X,P,M,N,K] =ndgrid(x,p,1:(num_max+1),1:(num_max+1),1:(num_max+1));
%and comment the following one:

[X,P,M,N] =ndgrid(x,p,1:(num_max+1),1:(num_max+1));
L=LaguerreMatrix(num_max);
W=zeros(length(x),length(p), num_max+1, num_max+1);
for k=1:num_max+1
W=W+(2-(M==N)).*(-1).^(M-1)./pi.*realsqrt(factorial(M-1)./factorial(N-1))...
    .*(2.*X.^2+2.*P.^2).^(abs(N-M)./2)...
    .*L(M+(num_max+1).*(N-1)+(num_max+1)^2.*(k-1))...
    .*(2.*X.^2+2*P.^2).^(k-1).*exp(-X.^2-P.^2)...
    .*real(rho_mle(M+(num_max+1).*(N-1)).*exp(i.*(N-M).*atan2(X,P)));
k
end
W3D=sum(sum(W,4),3);

%To vectorize K, comment the previous and uncomment the following:
%W3D=sum(sum(sum(W,5),4),3);

[X,P]=ndgrid(x,p);
figure(103)
surf(X,P,W3D)
hold on
shading interp
colormap(jet)
light
lighting phong
hold off   


