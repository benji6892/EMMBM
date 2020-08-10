""" Estimates the model with variable costs and plots all related graphs """

from simulation_Q_cv import *
from simulation_Q_base import *
from recuperation_donnees import charger_donnees
from estimation import *

R,P,Q,cours=charger_donnees()


#*******************************************************************************
#                             premiere periode
#*******************************************************************************

d=812 #debut
f=1483 #fin
r=0.1/365

lw=3

# les valeurs ci-dessous sont les bonnes
a=0.00316
B_tilde=23858
C0=2767

Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]
a,B_tilde,C0=estimation_a_B_tilde_C0(a,B_tilde,C0,R,Q,d,f)
Q_sim,P_sim=simulationQ_cv(a,B_tilde,Rp,Q0,C0)

x0=estimation_a_B_tilde(a,B_tilde,R,Q,d,f)
a_base=x0['x'][0]
B_tilde_base=x0['x'][1]
Q_sim_base,P_sim_base=simulationQ(a_base,B_tilde_base,Rp,Q0)
graphique_simulation_2(a,B_tilde,Q_sim,P_sim,Qp,Pp,Q_sim_base,d,f,type=(1,))

alpha,sigma2=estimation_alpha_sigma2(Rp)
I0=W0(a,B_tilde,C0,alpha,sigma2,r)
T=(1/a)*(log(B_tilde)-log(C0))
K0=I0+C0*(1-exp(-r*T))/r
print('B_tilde: ',B_tilde,'\nB_tilde_base: ',B_tilde_base,'\n')
print('a: ',365*a,'\nC0: ',C0,'\nI0: ',I0,'\nT: ',T/365,'\nTotal costs: ',\
      K0,'\n\n')
print('alpha: ',alpha,'\nsigma2: ',sigma2,'\n\n')



#*******************************************************************************
#                             deuxieme periode
#*******************************************************************************

d=2091 # start date 2nd period: 2091
f=3003 # end date 2nd period: 3003

r=0.1/365

# les valeurs ci-dessous sont les bonnes
a0=0.00207 # 0.00207
B_tilde0= 5.04 # 5.04
C0=0.683 # 0.683

Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]

a,B_tilde,C0=estimation_a_B_tilde_C0(a0,B_tilde0,C0,R,Q,d,f)

Q_sim,P_sim=simulationQ_cv(a,B_tilde,Rp,Q0,C0)

graphique_simulation_2(a,B_tilde,Q_sim,P_sim,Qp,Pp,Q_sim,d,f,type=(1,))


alpha,sigma2=estimation_alpha_sigma2(Rp)
I0=W0(a,B_tilde,C0,alpha,sigma2,r)
T=(1/a)*(log(B_tilde)-log(C0))
K0=I0+C0*(1-exp(-r*T))/r
print('B_tilde: ',B_tilde,'\n')
print('a: ',a,'\nC0: ',C0,'\nI0: ',I0,'\nT: ',T/365,'\nTotal costs: ',K0)
print('alpha: ',alpha,'\nsigma2: ',sigma2,'\n\n')






#*******************************************************************************
#                             troisième periode
#*******************************************************************************

##d=3369 # start date 3nd period: 3500 3369 3400
##f=3701 # end date 3nd period: 3701
##
##r=0.1/365
##
### les valeurs ci-dessous sont les bonnes
##a=0.00397 # 0.000488 0.00397 0.00378
##B_tilde= 0.545 # 0.2638 0.545 0.4718
##C0=0.15 # 0.07145 0.158 0.124
##
##Rp=R[d:f+1]
##Pp=P[d:f+1]
##Qp=Q[d:f+1]
##Q0=Q[d-1]
##a,B_tilde,C0=estimation_a_B_tilde_C0(a,B_tilde,C0,R,Q,d,f)
##
##Q_sim,P_sim=simulationQ_cv(a,B_tilde,Rp,Q0,C0)
##
##graphique_simulation_2(a,B_tilde,Q_sim,P_sim,Qp,Pp,Q_sim,d,f,type=(1,2))
##
##
##alpha,sigma2=estimation_alpha_sigma2(Rp)
##I0=W0(a,B_tilde,C0,alpha,sigma2,r)
##T=(1/a)*(log(B_tilde)-log(C0))
##K0=I0+C0*(1-exp(-r*T))/r
##print('B_tilde: ',B_tilde,'\n')
##print('a: ',a,'\nC0: ',C0,'\nI0: ',I0,'\nT: ',T/365,'\nTotal costs: ',K0)
##print('alpha: ',alpha,'\nsigma2: ',sigma2,'\n\n')
##print('d: ',d,'\ndate: ',date_str(d))
##print('f: ',f,'\ndate: ',date_str(f))


