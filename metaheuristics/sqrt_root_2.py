import math

def binary_root(a,b,error):
    """ This function computes the square root of 2 by continuously spliting the interval on two 
    """
    f=lambda x:x**2-2
        
    while abs(b-a)>error:
        c=(a+b)/2
        if f(a)*f(c)<=0:
            b=c
        else:
            a=c
    return a

  def newton_root(a,error):
    """ This function computes the square root of 2 by applying Newton formula x_(n+1)=x_n - f(x_n)/f'(x_n)
    """
    f=lambda x:x**2-2
    df=lambda x:2*x
    while True:
        b=a-f(a)/df(a)
        if abs(b-a)<error:break
        a=b
    return a

def hill_clibming_with_derivative(y0,eta,error):
    """This function maximizes the function f(x)=-(x^2-2)^2 whose optimum is reached for x=sqrt(2).
    Searching is made by using the gradient of f (its derivative).
    """
    derivative=lambda x:-4*x*(x**2-2) # this is the derivative of f
    y=y0
    for _ in range(200):
        ny=y+eta*derivative(y)
        if math.fabs(ny-y)<error:break
        y=ny
    return y

def hill_clibming_with_local_search(y0,eta):
    """This function maximizes the function f(x)=-(x^2-2)^2 whose optimum is reached for x=sqrt(2).
    Searching is made by using local search.
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


# print(binary_root)
# print(newton_root)
# print(hill_clibming_with_derivative(0.1,0.01,1e-7))
print(hill_clibming_with_local_search(0,0.05))
