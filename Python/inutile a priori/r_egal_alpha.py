from simulation_Q_cv import *
from simulation_Q_base import *
from recuperation_donnees import charger_donnees
from estimation import *

R,P,Q,cours=charger_donnees()

#*******************************************************************************
#                             deuxieme periode
#*******************************************************************************

d=2091 # start date 2nd period: 2091
f=3003 # end date 2nd period: 3003

# les valeurs ci-dessous sont les bonnes
a0=0.00207 # 0.00207
B_tilde0= 5.04 # 5.04
C0=0.1 # 0.683

Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]
a,B_tilde,C0=estimation_a_B_tilde_C0(a0,B_tilde0,C0,R,Q,d,f)

alpha0,sigma2=estimation_alpha_sigma2(Rp)

I0 = 900
print('alpha: ',estimation_alpha(I0,a,B_tilde,C0,sigma2,alpha0))


