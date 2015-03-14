function [val, grad] = f(x)
    val = (x-3)^2;
    grad = 2* (x - 3);
end    