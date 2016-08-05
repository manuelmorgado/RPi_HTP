function X = accrejrnd2(f,g,grnd,c,m)
               
X = zeros(m,2); % Preallocate memory
for i = 1:m
    accept = false;
    while accept == false
        u = rand();
        v = grnd();
        y = rand()*2*pi;
        if c*u <= f(v,y)/g(v)
           X(i,1) = v;
           X(i,2) = y;
           accept = true;
        end
    end
end