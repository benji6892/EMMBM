from simulation_Q_cv import *
from simulation_Q_base import *
from recuperation_donnees import charger_donnees
from estimation import *

R,P,Q,cours=charger_donnees()

d=1400 # start date 2nd period: 2091
f=2100 # end date 2nd period: 3003

a=0.013 # 0.00207
B_tilde= 68889 # 5.04
C0=0 # 0.683

Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]

couts,Q_pot,Q_eff = distribution_initiale(a,B_tilde,Q0,C0)
print(len(couts))

a,B_tilde,C0=estimation_a_B_tilde_C0(a,B_tilde,C0,R,Q,d,f)

Q_sim,P_sim=simulationQ_cv(a,B_tilde,Rp,Q0,C0)

graphique_simulation_2(a,B_tilde,Q_sim,P_sim,Qp,Pp,Q_sim,d,f,type=(1,))








