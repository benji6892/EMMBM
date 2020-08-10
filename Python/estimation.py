""" module qui permet d'estimer tous les parametres  Traite les cas avec et sans
couts variables """

from scipy.optimize import fsolve
from scipy.integrate import quad
from scipy.stats import *
from numpy import *
from datebase import *

#*******************************************************************************
#                               baseline model
#*******************************************************************************

def estimation_alpha_sigma2(Rp):

    """ fonction qui estime alpha et sigma2 par maximum de vraisemblance.
    Bien reflechir a ce que doit etre Rp: R sur toute la periode ou bien
    r sur la periode d'etude seulement? """
    
    M=diff(log(Rp))
    sigma2=var(M)
    alpha=mean(M)+0.5*sigma2
    return alpha,sigma2

def IC(Rp,quantile=0.95):

    """ fonction qui calcule des intervalles de confiance asymptotiques
    pour mu et sigma2.
    quantile: niveau de confiance. """
    n=len(Rp)
    M=diff(log(Rp))
    sigma2=var(M)
    mu=mean(M)
    qn=norm.ppf((1+quantile)/2) # quantile loi normale
    return [mu-qn*sqrt(sigma2/n),mu+qn*sqrt(sigma2/n)],\
           [sigma2*(1-qn/sqrt(n)),sigma2*(1+qn/sqrt(n))]

def estimation_alpha_sigma2_tronquee(Rp,trim=0.05):

    """ fonction qui estime alpha et sigma2 par maximum de vraisemblance.
    On enleve les rendements les 2.5% plus petits et 2.5% plus grands
    (quand trim = 0.05) """
    
    N=sorted(diff(log(Rp)))
    M=N[int(floor(len(N)*trim/2)):int(floor(len(N)*(1-trim/2)))]
    sigma2=var(M)
    mu=mean(N)   
    alpha=mu+0.5*sigma2
    return alpha,sigma2

def estimation_alpha_sigma2_tronquee_plot(Rp,trim=0.05):

    """ same as before with a plot"""
    
    N=sorted(diff(log(Rp)))
    M=N[int(floor(len(N)*trim/2)):int(floor(len(N)*(1-trim/2)))]
    sigma2=var(M)
    mu=mean(N) 
    print('mu: ',mu)
    alpha=mu+0.5*sigma2
    densite_M=gaussian_kde(M)
    plage=arange(min(N),max(N),(max(N)-min(N))/100)
    fun=lambda x: exp(-(x-mu)**2/(2*sigma2))/(sqrt(2*pi*sigma2))
    plot(plage,densite_M.evaluate(plage),'b')
    plot(plage,fun(plage),'r')
    show()
    return alpha,sigma2

def expr_beta(alpha,sigma2,a,r):

    """ fonction qui calcule beta defini dans le modele """
    
    A=(alpha+a-0.5*sigma2)**2+2*sigma2*a
    B=alpha+a
    return (0.5*sigma2-B+sqrt(A+2*sigma2*r))/sigma2

def estimation_CT(a,alpha,sigma2,B_tilde,r):

    """ estimation des couts totaux en fixant r """
    
    beta=expr_beta(alpha,sigma2,a,r)
    return B_tilde*(beta-1)/(beta*(r-alpha))
    
    
#*******************************************************************************
#                        modele avec couts variables
#*******************************************************************************

def densite_Ps(x,s,a,B_tilde,alpha,sigma2):

    """ densite de P dans s periodes. Aujourd'hui, P=B """

    deno=sqrt(sigma2*s)
    A=(1/deno)*norm.pdf((log(B_tilde)-log(x)+(alpha-0.5*sigma2)*s)/deno)
    B=exp((log(B_tilde)-log(x)-a*s)*(1-2*((a+alpha)/sigma2)))
    C=(2*((a+alpha)/sigma2)-1)*\
       norm.cdf((log(x)-log(B_tilde)+(2*a+alpha-0.5*sigma2)*s)/deno)
    D=(1/deno)*norm.pdf((log(x)-log(B_tilde)+(2*a+alpha-0.5*sigma2)*s)/deno)
    return (1/x)*(A+B*(C+D))


def esp_profit_cv(s,a,B_tilde,C0,alpha,sigma2):

    """ Substep (inner integral) in the computation of W0 (function below). """
    
    integral = quad(lambda x: (x-C0)*densite_Ps(x,s,a,B_tilde,alpha,sigma2),\
         C0, B_tilde*exp(-a*s),epsrel=0.01)
    return integral[0]


def W0(a,B_tilde,C0,alpha,sigma2,r):

    """ value function at t=0 when P=B_tilde. Due to free entry,
    in the model, this quantity is equal to I0. """
    
    T=(1/a)*(log(B_tilde)-log(C0))
    integral = quad(lambda s: esp_profit_cv(s,a,B_tilde,\
                                            C0,alpha,sigma2)*exp(-r*s),0, T,\
                    epsrel=0.01)
    return integral[0]

def Newton_Raphson(f,x1):
    """ Newton-Raphson algorithm with approximated derivative. Finds x such that f(x)=0 """
    eps=0.00001
    x0=x1+1
    while(abs(x1-x0)>eps):
        x0=x1
        f0=f(x0)
        x1=x0-f0*eps/(f(x0+eps)-f0)
    return x1

def estimation_alpha(I0,a,B_tilde,C0,sigma2,alpha0):
    return Newton_Raphson(lambda alpha: I0 - W0(a,B_tilde,C0,alpha,sigma2,alpha), alpha0)


#*******************************************************************************
#                        modele avec delais
#*******************************************************************************

def estimation_CT_delay(a,delta,alpha,sigma2,B_tilde,r):

    """ estimation des couts totaux en fixant r """
    
    beta=expr_beta(alpha,sigma2,a,r)
    return B_tilde*(beta-1)/(beta*(r-alpha))*exp((r-alpha)*delta)
