function loss=loss(m,k,eta)
%This function accounts for loss in the Homodyne POVMs
loss=(m>=k).*realsqrt(factorial(m)./factorial(k)./factorial(abs(m-k)).*eta.^abs(m-k).*(1-eta).^k);
