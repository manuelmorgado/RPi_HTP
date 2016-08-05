function X = accrejrnd(f,g,grnd,c,m)
               
X = zeros(m,2); % Preallocate memory
for i = 1:m
    accept = false;
    while accept == false
        u = rand();
        v = grnd();
        if c*u <= f(v)/g(v)
           X(i,1) = sign(rand()-0.5)*v;
           X(i,2) = 2*pi*rand();
           accept = true;
        end
    end
end