""" modele deterministe avec cout variable et calculs sur la securite """

from numpy import *
from scipy.stats import norm
from scipy.integrate import quad,dblquad
from scipy.optimize import fsolve
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D
import pickle
from estimation import *

I2011=180/0.0003     # 722
I2012=180/0.00068    # 1087
I2012bis=170/0.00022
I2013=1300/0.0663    # 1453
I2014=300/0.18       # 1818
I2015=370/1.15       # 2183
I2016=1823/4.86      # 2548
I2017=2400/14        # 2914

C2011=0.17*24*0.05/0.0003
C2012=0.17*24*0.05/0.00068
C2012bis=0.01*24*0.05/0.00022
C2013=0.62*24*0.05/0.0663
C2014=0.36*24*0.05/0.18
C2015=0.59*24*0.05/1.15
C2016=1.21*24*0.05/4.86
C2017=1.375*24*0.05/14

a=log(2)/730 # loi de Moore
r=0.05/365

with open('donnees', 'rb') as fichier:
    mon_depickler = pickle.Unpickler(fichier)
    R=mon_depickler.load()
    P=mon_depickler.load()
    Q=mon_depickler.load()
    cours=mon_depickler.load()

def fun_R(R,S,D,a,r):   # D=I/C
    T=log(R*D/S)/a
    return (S-S*(exp(-r*T)-1)/(D*r))*(a+r)/(1-exp(-(a+r)*T))-R

def fun_find_R(S,D,a,r):
    return fsolve(lambda R: fun_R(R,S,D,a,r),S*(1+500/D)*(a+r))[0]

D=1000

print('2011: ',fun_find_R(I2011*Q[722],D,a,r)/(144*2000))
#print('2012: ',fun_find_R(I2012*Q[1087],D,a,r)/(144*2000))
print('2013: ',fun_find_R(I2013*Q[1453],D,a,r)/(144*2000))
print('2014: ',fun_find_R(I2014*Q[1818],D,a,r)/(144*2000))
print('2015: ',fun_find_R(I2015*Q[2183],D,a,r)/(144*2000))
print('2016: ',fun_find_R(I2016*Q[2543],D,a,r)/(144*2000))
print('2017: ',fun_find_R(I2017*Q[2914],D,a,r)/(144*2000))

