"""Estimates the baseline model and plots all related graphs"""

from simulation_Q_constrained import *
from simulation_Q_base import *
from recuperation_donnees import charger_donnees
from estimation import estimation_alpha_sigma2, IC, estimation_CT
from matplotlib.dates import *

R,P,Q,cours=charger_donnees() # load the data.


#*******************************************************************************
#                             first period
#*******************************************************************************

##print('\npremiere periode\n')
##
##d=812 #start date 812
##f=1483 #end date 1483
##
##r=0.1/365 # daily discount rate (ex: 0.1/365 corresponds to 10% annually)
##
### initial values for the parameters for the estimation
##a=0.0032334
##B_tilde=25996
##const=2
##
### select only the time laps we are interested in
##Rp=R[d:f+1]
##Pp=P[d:f+1]
##Qp=Q[d:f+1]
##Q0=Q[d-1]
##
##x0=estimation_a_B_tilde_fixedconstrained(a,B_tilde,const,R,Q,d,f)
### estimated values
##a=x0['x'][0]
##B_tilde=x0['x'][1]
##
##Q_sim,P_sim=simulationQconstrained(a,B_tilde,const,Rp,Q0)
##graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,type=(1,2))
##plot_cours(cours,d,f)
##
##alpha,sigma2=estimation_alpha_sigma2(Rp)
##intervalle=IC(Rp,0.95)
##
##print('parametres annuels\n')
##
##mu=alpha-0.5*sigma2
##print('mu: ',365*mu)
##print([365*i for i in intervalle[0]])
##print('\nsigma2: ',365*sigma2)
##print([365*i for i in intervalle[1]])
##print('\na: ',a,'\n')
##print('r fixe: ',r,'\n')
##
##print('couts totaux: ',estimation_CT(a,alpha,sigma2,B_tilde,r),'\n')
##print('d: ',d,'\ndate: ',date_str(d))
##print('f: ',f,'\ndate: ',date_str(f))
####
###*******************************************************************************
###                             second periode
###*******************************************************************************

print('**********************************\ndeuxieme periode\n')

d=2091 #start date 2091
f=len(R) - 1 #end date 3003 

r=0.1/365 

a=0.00207
B_tilde=5.3
const=2

Rp=R[d:f+1]
Pp=P[d:f+1]

Qp=Q[d:f+1]
Q0=Q[d-1]

x0=estimation_a_B_tilde_fixedconstrained(a,B_tilde,const,R,Q,d,f)
a=x0['x'][0]
B_tilde=x0['x'][1]
print('a: ',a)
print('B_tilde: ',B_tilde)

Q_sim,P_sim=simulationQconstrained(a,B_tilde,const,Rp,Q0)
graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,type=(1,2))
plot_cours(cours,d,f)

alpha,sigma2=estimation_alpha_sigma2(Rp)
intervalle=IC(Rp,0.95)

print('parametres annuels\n')

mu=alpha-0.5*sigma2
print('mu: ',365*mu)
print([365*i for i in intervalle[0]])
print('\nsigma2: ',365*sigma2)
print([365*i for i in intervalle[1]])
print('\na: ',a,'\n')
print('r fixe: ',r,'\n')

print('couts totaux: ',estimation_CT(a,alpha,sigma2,B_tilde,r),'\n')
print('d: ',d,'\ndate: ',date_str(d))
print('f: ',f,'\ndate: ',date_str(f))

###*******************************************************************************
###                             troisieme periode
###*******************************************************************************

##print('**********************************\ntroisieme periode\n')
##
##d=3369 #start date 2091
##f=3701 #end date 3003 
##
##r=0.1/365 
##
##a=0.004
##B_tilde=0.25
##const = 2
##
##Rp=R[d:f+1]
##Pp=P[d:f+1]
##Qp=Q[d:f+1]
##Q0=Q[d-1]
##
##x0=estimation_a_B_tilde_fixedconstrained(a,B_tilde,const,R,Q,d,f)
##a=x0['x'][0]
##B_tilde=x0['x'][1]
##print('a: ',a)
##print('B_tilde: ',B_tilde)
##
##Q_sim,P_sim=simulationQconstrained(a,B_tilde,const,Rp,Q0)
##graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,type=(1,2))
##plot_cours(cours,d,f)
##
##alpha,sigma2=estimation_alpha_sigma2(Rp)
##intervalle=IC(Rp,0.95)
##
##print('parametres annuels\n')
##
##mu=alpha-0.5*sigma2
##print('mu: ',365*mu)
##print([365*i for i in intervalle[0]])
##print('\nsigma2: ',365*sigma2)
##print([365*i for i in intervalle[1]])
##print('\na: ',a,'\n')
##print('r fixe: ',r,'\n')
##
##print('couts totaux: ',estimation_CT(a,alpha,sigma2,B_tilde,r),'\n')































