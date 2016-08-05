function X=Fock_one_eff(eff, num_data)
%This generates num_data elements of fake balanced homodyne data of a one photon state, where the photodiode has efficiency eff. The output is X(j,1)=x(j) (i.e. the difference signal) and
%X(j,2)=theta(j) (i.e. the phase of the local oscillator). It models
%efficiency as rho=eff*1><1 + (1-eff)*0><0 
%Single photon part of the mixture
f = @(x)(exp(-x.^2).*(2/pi)^(1/4)./realsqrt(2).*2*realsqrt(2).*x).^2;
g = @(x)1;
grnd = @()rand(1).*10;
%Vacuum part
W = accrejrnd(f,g,grnd,1,round(num_data*eff));
h = @(x)(exp(-x.^2).*(2/pi)^(1/4)).^2;
Y = accrejrnd(h,g,grnd,1,round(num_data*(1-eff)));
X=vertcat(W,Y);