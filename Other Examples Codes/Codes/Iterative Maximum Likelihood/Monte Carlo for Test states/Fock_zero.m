function X=Fock_zero(num_data)
%This generates num_data elements of fake balanced homodyne data of a vacuum state. The output is X(j,1)=x(j) (i.e. the difference signal) and
%X(j,2)=theta(j) (i.e. the phase of the local oscillator). [x,p]=i/2
g = @(x)1;
grnd = @()rand(1).*10;
h = @(x)(exp(-x.^2).*(2/pi)^(1/4)).^2;
X = accrejrnd(h,g,grnd,1,num_data);
