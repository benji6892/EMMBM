""" local linear regression with gaussian kernel """

import numpy as np

k = lambda x: [np.exp(-a**2/2)/np.sqrt(2*np.pi) for a in x]

def local_linear_regression(y,x,h):

    # h: window.

    res=[]
    x=np.array(x)
    y=np.array(y)
    for a in x:
        d=a-x
        z=k(d/h)
        s1=d*z
        s2=sum(d*s1)
        s1=sum(s1)
        res.append(sum((s2-s1*d)*z*y)/(s2*sum(z)-s1*s1))

    return res

if __name__== "__main__": # for tests purposes.
    import matplotlib.pyplot
    x=arange(1,101)
    y=x**2/100+10*random.randn(100)
    h=7
    f=local_linear_regression(y,x,h)
    matplotlib.pyplot.plot(x,f,x,y)
    matplotlib.pyplot.show()
