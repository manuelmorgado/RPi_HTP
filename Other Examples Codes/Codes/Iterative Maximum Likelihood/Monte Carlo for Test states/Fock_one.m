function X=Fock_one(num_data)
%This generates num_data elements of fake balanced homodyne data of a one photon state. The output is X(j,1)=x(j) (i.e. the difference signal) and
%X(j,2)=theta(j) (i.e. the phase of the local oscillator)
f = @(x)(exp(-x.^2).*(2/pi)^(1/4)./realsqrt(2).*2*realsqrt(2).*x).^2;

g = @(x)1;
grnd = @()rand(1).*10;
X = accrejrnd(f,g,grnd,1,num_data);