import math
import random

def binary_search_root(a,b,error):
    """ This function computes the square root of 2 by continuously splitting the interval on two 
    """
    f=lambda x:x**2-2
    nb=0   
    while abs(b-a)>error:
        c=(a+b)/2
        if f(a)*f(c)<=0:
            b=c
        else:
            a=c
        nb+=1
    return c,nb

def newton_root(a,error):
    """ This function computes the square root of 2 by applying Newton formula x_(n+1)=x_n - f(x_n)/f'(x_n)
    """
    f=lambda x:x**2-2
    df=lambda x:2*x
    nb=0
    while True:
        b=a-f(a)/df(a)
        if abs(b-a)<error:break
        a=b
        nb+=1
    return a,nb

def hill_clibming_with_derivative_root(y0,eta,error):
    """This function maximizes the function f(x)=-(x^2-2)^2 whose optimum is reached for x=sqrt(2).
    Searching is made by using the gradient of f (its derivative).
    eta: is a parameter that controls how the gradient acts on the search (eta in [0,1])
    """
    derivative=lambda x:-4*x*(x**2-2) # this is the derivative of f
    y=y0
    nb=0
    for _ in range(200):
        ny=y+eta*derivative(y)
        if math.fabs(ny-y)<error:break
        y=ny
        nb+=1
    return y,nb

def hill_clibming_with_local_search_root(y0,eta):
    """This function maximizes the function f(x)=-(x^2-2)^2 whose optimum is reached for x=sqrt(2).
    Searching is made by using local search.
    eta: is used here to control the width of the neighborhood
    """
    f=lambda x:-(x**2-2)**2
    y=y0
    best=f(y)
    for _ in range(200):
        h={(z:=max(y+(random.random()-0.5)*eta,0)):f(z) for _ in range(10)}
        cand=max(h,key=h.get)
        if best<h[cand]:
            best=h[cand]
            y=cand
    return y

print(binary_search_root(0,2,1e-7))
print(newton_root(0.1,1e-7))
print(hill_clibming_with_derivative_root(0.1,0.01,1e-7))
print(hill_clibming_with_local_search_rrot(0,0.05))
