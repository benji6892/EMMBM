""" module qui contient les fonctions qui utilisent les modeles pour repondre
a des questions interessantes sur Bitcoin """

from numpy import *
from scipy.stats import norm
from scipy.integrate import quad,dblquad
from scipy.optimize import fsolve
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D
import pickle
from estimation import *

def fdr_Qt_It(x,t,y,a,alpha,sigma2):

    """ fonction de repartition de QtIt/Q0I0 conditionnellement
        a y = P0/B_tilde """

    if x<exp(-a*t):
        return 0
    else:
        deno=sqrt(sigma2*t)
        z=log(x)-log(y)+a*t
        mu=alpha-0.5*sigma2
        return norm.cdf((z-(mu+a)*t)/deno)-\
               exp(2*(mu+a)*z/sigma2)*norm.cdf((-z-(mu+a)*t)/deno)

def esp_Qt_It(t,y,a,alpha,sigma2):

    """ esperance de QtIt/Q0I0 conditionnellement a y = P0/B_tilde """

    return quad(lambda x: 1-fdr_Qt_It(x,t,y,a,alpha,sigma2),\
                0,10*exp(alpha*t))[0]

def quantile_Qt_It(q,t,y,a,alpha,sigma2):

    """ quantile de QtIt/Q0I0 conditionnellement a y = P0/B_tilde """

    if fdr_Qt_It(exp(-a*t),t,y,a,alpha,sigma2) > q:
        return exp(-a*t)
    else:
        return fsolve(lambda x: fdr_Qt_It(x,t,y,a,alpha,sigma2)-q,1)[0]

def quantile_Qt_It_bis(q,t,y,a,alpha,sigma2):

    """ quantile de QtIt/Q0I0 non conditionnelle """
    if fdr_Qt_It(exp(-a*t),t,y,a,alpha,sigma2) > q:
        return exp(-a*t)
    else:
        xi=exp(-a*t)
        xs=1
        while xs-xi>0.0001:
            xm=(xs+xi)/2
            if fdr_Qt_It(xm,t,y,a,alpha,sigma2) > q:
                xs=xm
            else:
                xi=xm
        return xs

def densite_ergodique(y,alpha,sigma2,a):

    """ densite ergodique de P0/B_tilde """
    return (alpha+a-0.5*sigma2)*y**((alpha+a-1.5*sigma2)/sigma2)/sigma2

def fdr_Qt_It2(x,t,a,alpha,sigma2):

    """ fonction de repartition de QtIt/Q0I0 non conditionnelle """
    return quad(lambda y: fdr_Qt_It(x,t,y,a,alpha,sigma2)*\
         densite_ergodique(y,alpha,sigma2,a),0,1)[0]

def esp_Qt_It2(t,a,alpha,sigma2):

    """ esperance de QtIt/Q0I0 non conditionnelle """
    return quad(lambda x: 1-fdr_Qt_It2(x,t,a,alpha,sigma2),\
                0,10*exp(alpha*t))[0]    

def quantile_Qt_It2(q,t,a,alpha,sigma2):

    """ quantile de QtIt/Q0I0 non conditionnelle """

    if fdr_Qt_It2(exp(-a*t),t,a,alpha,sigma2) > q:
        return exp(-a*t)
    else:
        return fsolve(lambda x: fdr_Qt_It2(x,t,a,alpha,sigma2)-q,1)[0]

def quantile_Qt_It2_bis(q,t,a,alpha,sigma2):

    """ quantile de QtIt/Q0I0 non conditionnelle """
    if fdr_Qt_It2(exp(-a*t),t,a,alpha,sigma2) > q:
        return exp(-a*t)
    else:
        xi=exp(-a*t)
        xs=1
        while xs-xi>0.0001:
            xm=(xs+xi)/2
            if fdr_Qt_It2(xm,t,a,alpha,sigma2) > q:
                xs=xm
            else:
                xi=xm
        return xs

#******************************************************************************    

with open('donnees', 'rb') as fichier:
    mon_depickler = pickle.Unpickler(fichier)
    R=mon_depickler.load()
    P=mon_depickler.load()
    Q=mon_depickler.load()
    cours=mon_depickler.load()

d=2091
f=3003
Rp=R[d:f+1]

t=365*10 #duree au bout de laquelle on regarde QtIt/Q0I0
print('\nhorizon temporel: ',t/365,' ans')
q=0.33 # quantile de la distribution qui nous interesse
y=1

#*************************  parametres actuels  *******************************

print('\nparametres actuels\n')
alpha,sigma2=estimation_alpha_sigma2_tronquee(Rp,trim=0.05)
mu=alpha-0.5*sigma2
a=0.0024054
r=0.05/365

#*******************************************************************************
#                    constante devant l'exponentielle
#*******************************************************************************

I0=1 # aucune importance
print('constante: ',I0/expr_B_tilde(r,I0,a,mu+0.5*sigma2,sigma2))


#*************************  parametres futurs  *******************************
print('\n\n\nparametres futurs\n')
alpha,sigma2=estimation_alpha_sigma2_tronquee(Rp,trim=0.05)
mu=0
a=log(2)/730
r=0.05/365

#*******************************************************************************
#                    constante devant l'exponentielle
#*******************************************************************************

I0=1 # aucune importance
print('constante: ',I0/expr_B_tilde(r,I0,a,mu+0.5*sigma2,sigma2))

