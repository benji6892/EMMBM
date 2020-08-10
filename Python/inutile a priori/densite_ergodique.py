""" module qui compare la densite ergodique observee de P_t/B_t avec celle
    predite """

# Pour l'instant c'est mal fait. Par exemple, il faudrait utiliser un autre
# noyau ou bien une autre bandwidth car la densite a un saut...
# Mais comme ca ne marche pas du tout: je n'ai pas passe trop de temps la-
# dessus pour l'instant.

from numpy import *
from matplotlib.pyplot import *
import pickle
from simulation_Q import *
from estimation import *
from scipy.stats import *

with open('donnees', 'rb') as fichier:
    mon_depickler = pickle.Unpickler(fichier)
    R=mon_depickler.load()
    P=mon_depickler.load()
    Q=mon_depickler.load()

#periode d'estimation des parametres
d=722
f=1483

a0=0.0034209 #0.0024054
B_tilde0=33504 #5.32

# on estime a et B0
x0=estimation_a_B_tilde(a0,B_tilde0,1,R,Q,d,f,simulationQ)
a=x0['x'][0]
B_tilde=x0['x'][1]

# on estime alpha et sigma2
alpha,sigma2=estimation_alpha_sigma2_tronquee(R[d:f+1],trim=0.05)

Bt=B_tilde/exp(a*arange(1,f-d+2))
Pt=P[d:f+1]
data=[p/b for p,b in zip(Pt,Bt)]
data=[min(1,d) for d in data] # on redescend le payoff a 1 toutes les fois
# ou il depasse la barriere
densite_data=gaussian_kde(data)

# densite theorique
fun=lambda x: (x>0)*(x<1)*\
     (alpha+a-0.5*sigma2)*x**((alpha+a-0.5*sigma2)/sigma2)/sigma2


plot(arange(0,1.7,0.01),densite_data.evaluate(arange(0,1.7,0.01)),'r')
plot(arange(0,1.7,0.01),fun(arange(0,1.7,0.01)),'b')
show()
