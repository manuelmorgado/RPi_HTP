function HO=HO(m,x,theta)
%The mth harmonic oscillator state=HO(m,x,theta)*H_m(sqrt(2)*x), where H_m is the mth Hermite Polynomial 
HO=exp(i*m.*theta-x.^2).*(2/pi)^(1/4)./realsqrt(2.^m.*factorial(abs(m)));
