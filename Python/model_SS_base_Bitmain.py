"""Estimates the baseline model and plots all related graphs"""

from simulation_Q_Bitmain import *
from recuperation_donnees import charger_donnees
from estimation import estimation_alpha_sigma2, IC, estimation_CT
from matplotlib.dates import *

R,P,Q,cours=charger_donnees() # load the data.



###*******************************************************************************
###                             second periode
###*******************************************************************************

print('**********************************\ndeuxieme periode\n')


d=2091 #start date 2091
f=3003 #end date 3003 


#d=2091 #start date 2091
#f=3003 #end date 3003 
#f=3803 #end date 3003 

r=0.1/365 

a=0.00207
B_tilde=5.3
Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]

x0=estimation_a_B_tilde(a,B_tilde,R,Q,d,f)
a=x0['x'][0]
B_tilde=x0['x'][1]
print('a: ',a)
print('B_tilde: ',B_tilde)

Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
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



##
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
##Rp=R[d:f+1]
##Pp=P[d:f+1]
##Qp=Q[d:f+1]
##Q0=Q[d-1]
##
##x0=estimation_a_B_tilde(a,B_tilde,R,Q,d,f)
##a=x0['x'][0]
##B_tilde=x0['x'][1]
##print('a: ',a)
##print('B_tilde: ',B_tilde)
##
##Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
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































