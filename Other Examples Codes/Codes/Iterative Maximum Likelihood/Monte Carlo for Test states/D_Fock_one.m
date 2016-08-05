function X=D_Fock_one(alpha, num_data)
%This generates num_data elements of fake balanced homodyne data of a one photon state displaced by alpha (which
%is complex). The output is X(j,1)=x(j) (i.e. the difference signal) and
%X(j,2)=theta(j) (i.e. the phase of the local oscillator)
f = @(x,theta)(exp(-(x-abs(alpha).*cos(theta-angle(alpha))).^2).*(2/pi)^(1/4)./realsqrt(2).*2*realsqrt(2).*(x-abs(alpha).*cos(theta-angle(alpha)))).^2;

g = @(x)1;
grnd = @()(5-rand(1).*10);
X = accrejrnd2(f,g,grnd,1,num_data);