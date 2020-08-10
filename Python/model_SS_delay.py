"""Estimates the baseline model and plots all related graphs"""

from simulation_Q_delay import *
from recuperation_donnees import charger_donnees
from estimation import estimation_alpha_sigma2, IC, estimation_CT_delay
from matplotlib.dates import *

R,P,Q,cours=charger_donnees() # load the data.


###*******************************************************************************
###                             first periode
###*******************************************************************************

print('**********************************\npremiere periode\n')


d=812 #start date 2091
f=1483 #end date 3003 

r=0.1/365 

a_init=0.004
B_tilde_init=26000
delta_opt=11

Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]

#Rp_illustration=R[d:f+500]
#Pp_illustration=P[d:f+500]
#Qp_illustration=Q[d:f+500]



""" Optimization """
x0=estimation_payoff_delay(a_init,B_tilde_init,delta_opt,R,Q,P,d,f)
#x0=estimation_relative_payoff_delay(a_init,B_tilde_init,delta_opt,R,Q,P,d,f)

a_delay=x0['x'][0]
B_tilde_delay=x0['x'][1]
delta=x0['x'][2]
print('a: ',a_delay)
print('B_tilde: ',B_tilde_delay)
print('delta: ',delta)

##x0relative=estimation_relative_payoff_delay(a_init,B_tilde_init,delta_opt,R,Q,P,d,f)
##arelative_delay=x0relative['x'][0]
##B_tilderelative_delay=x0relative['x'][1]
##deltarelative=x0relative['x'][2]
##print('a_relative: ',arelative_delay)
##print('B_tilde_relative: ',B_tilderelative_delay)
##print('delta_relative: ',deltarelative)


C_sim_delay,Q_sim_delay,P_sim_delay=simulationQdelay(a_delay,B_tilde_delay,delta,Rp,Q0)
graphique_simulation_delay(a_delay,B_tilde_delay,delta,Q_sim_delay,P_sim_delay,Qp,Pp,d,f,type=(1,2))


#C_sim,Q_sim,P_sim=simulationQdelay(a,B_tilde,delta,Rp_illustration,Q0)
#graphique_simulation_delay(a,B_tilde,delta,Q_sim,P_sim,Qp_illustration,Pp_illustration,d,f+499,type=(1,2))

#Crelative_sim,Qrelative_sim,Prelative_sim=simulationQdelay(arelative,B_tilderelative,deltarelative,Rp_illustration,Q0)
#graphique_simulation_delay(arelative,B_tilderelative,deltarelative,Qrelative_sim,Prelative_sim,Qp_illustration,Pp_illustration,d,f+499,type=(1,2))

##Crelative_sim,Qrelative_sim,Prelative_sim=simulationQdelay(arelative_delay,B_tilderelative_delay,deltarelative,Rp,Q0)

##graphique_simulation_delay(arelative_delay,B_tilderelative_delay,deltarelative,Qrelative_sim,Prelative_sim,Qp,Pp,d,f,type=(1,2))

alpha,sigma2=estimation_alpha_sigma2(Rp)
intervalle=IC(Rp,0.95)

print('parametres annuels\n')

mu=alpha-0.5*sigma2
print('mu: ',365*mu)
print([365*i for i in intervalle[0]])
print('\nsigma2: ',365*sigma2)
print([365*i for i in intervalle[1]])
print('\na: ',a_delay,'\n')
print('r fixe: ',r,'\n')
print('delay: ',delta,'\n')

print('couts totaux: ',estimation_CT_delay(a_delay,delta,alpha,sigma2,B_tilde_delay,r),'\n')


###*******************************************************************************
###                             second periode
###*******************************************************************************

print('**********************************\ndeuxieme periode\n')


d=2091 #start date 2091
f=3750 #end date 3003 

r=0.1/365 

a_init=0.003
B_tilde_init=5
delta_init=50

Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]

#Rp_illustration=R[d:f+500]
#Pp_illustration=P[d:f+500]
#Qp_illustration=Q[d:f+500]

#x0=estimation_a_B_tilde_delta(a,B_tilde,delta,R,Q,d,f)
#a=x0['x'][0]
#B_tilde=x0['x'][1]
#delta=x0['x'][2]
#print('a: ',a)
#print('B_tilde: ',B_tilde)
#print('delta: ',delta)

""" Grid search with delta fixed """
##objective_list=[]
##for i in range(1,50):
##    print(i)
##    xlist=estimation_relative_payoff_delay(a_init,B_tilde_init,i,R,Q,P,d,f)
##    objective_list.append(xlist.fun)

#delta_opt = objective_list.index(min(objective_list))+1
delta_opt = 49
   


""" Optimization """
x0=estimation_payoff_delay(a_init,B_tilde_init,delta_opt,R,Q,P,d,f)
#x0=estimation_relative_payoff_delay(a_init,B_tilde_init,delta_opt,R,Q,P,d,f)

a_delay=x0['x'][0]
B_tilde_delay=x0['x'][1]
delta=x0['x'][2]
print('a: ',a_delay)
print('B_tilde: ',B_tilde_delay)
print('delta: ',delta)

##x0relative=estimation_relative_payoff_delay(a_init,B_tilde_init,delta_opt,R,Q,P,d,f)
##arelative_delay=x0relative['x'][0]
##B_tilderelative_delay=x0relative['x'][1]
##deltarelative=x0relative['x'][2]
##print('a_relative: ',arelative_delay)
##print('B_tilde_relative: ',B_tilderelative_delay)
##print('delta_relative: ',deltarelative)


C_sim_delay,Q_sim_delay,P_sim_delay=simulationQdelay(a_delay,B_tilde_delay,delta,Rp,Q0)
graphique_simulation_delay(a_delay,B_tilde_delay,delta,Q_sim_delay,P_sim_delay,Qp,Pp,d,f,type=(1,2))


#C_sim,Q_sim,P_sim=simulationQdelay(a,B_tilde,delta,Rp_illustration,Q0)
#graphique_simulation_delay(a,B_tilde,delta,Q_sim,P_sim,Qp_illustration,Pp_illustration,d,f+499,type=(1,2))

#Crelative_sim,Qrelative_sim,Prelative_sim=simulationQdelay(arelative,B_tilderelative,deltarelative,Rp_illustration,Q0)
#graphique_simulation_delay(arelative,B_tilderelative,deltarelative,Qrelative_sim,Prelative_sim,Qp_illustration,Pp_illustration,d,f+499,type=(1,2))

##Crelative_sim,Qrelative_sim,Prelative_sim=simulationQdelay(arelative_delay,B_tilderelative_delay,deltarelative,Rp,Q0)
##graphique_simulation_delay(arelative_delay,B_tilderelative_delay,deltarelative,Qrelative_sim,Prelative_sim,Qp,Pp,d,f,type=(1,2))

alpha,sigma2=estimation_alpha_sigma2(Rp)
intervalle=IC(Rp,0.95)

print('parametres annuels\n')

mu=alpha-0.5*sigma2
print('mu: ',365*mu)
print([365*i for i in intervalle[0]])
print('\nsigma2: ',365*sigma2)
print([365*i for i in intervalle[1]])
print('\na: ',a_delay,'\n')
print('r fixe: ',r,'\n')
print('delay: ',delta,'\n')

print('couts totaux: ',estimation_CT_delay(a_delay,delta,alpha,sigma2,B_tilde_delay,r),'\n')














































