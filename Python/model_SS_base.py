"""Estimates the baseline model and plots all related graphs"""

from simulation_Q_base import *
from recuperation_donnees import charger_donnees
from estimation import estimation_alpha_sigma2, IC, estimation_CT
from matplotlib.dates import *
from xlwt import Workbook

R,P,Q,cours=charger_donnees() # load the data.


###*******************************************************************************
###                             first period
###*******************************************************************************
##
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
##
### select only the time laps we are interested in
##Rp=R[d:f+1]
##Pp=P[d:f+1]
##Qp=Q[d:f+1]
##Q0=Q[d-1]
##
##x0=estimation_a_B_tilde(a,B_tilde,R,Q,d,f)
### estimated values
##a=x0['x'][0]
##B_tilde=x0['x'][1]
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
###
###print('couts totaux: ',estimation_CT(a,alpha,sigma2,B_tilde,r),'\n')
##
###*******************************************************************************
###                             second periode
###*******************************************************************************

##print('**********************************\ndeuxieme periode\n')
##
##
##d=2091 #start date 2091
##f=3003 #end date 3003 
##
##
###d=2091 #start date 2091
###f=3003 #end date 3003 
###f=3803 #end date 3003 
##
##r=0.1/365 
##
##a=0.00207
##B_tilde=5.3
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

###*******************************************************************************
###                             third periode
###*******************************************************************************

print('**********************************\ndeuxieme periode\n')


d=3491 #start date 2091
f=4271 #end date 4271
print(date_str(d))

#d=2091 #start date 2091
#f=3003 #end date 3003 
#f=3803 #end date 3003 

r=0.1/365 

a=0.002
B_tilde=0.6
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




#####*******************************************************************************
#####                     second period and bubble (+ export)
#####*******************************************************************************
##
##
##d=2091 
##f=3850  
##
### parametres estimes sur la deuxieme periode.
##a=0.00207
##B_tilde=5.3
##Rp=R[d:f+1]
##Q0=Q[d-1]
##
##Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
##
##book=Workbook()
##estimation = book.add_sheet('estimation')
##dates = book.add_sheet('toutes les dates')
##estimation.write(0, 0, 'dates')
##estimation.write(0, 1, 'log Q simule')
##estimation.write(0, 2, 'P simule')
##for t in range(0, len(Q_sim)):
##    estimation.write(t+1, 0, date_str(d+t))
##    estimation.write(t+1, 1, log(Q_sim[t]))
##    estimation.write(t+1, 2, P_sim[t]     )
##
##for t in range(0, len(R)):
##    dates.write(t, 0, t)
##    dates.write(t, 1, date_str(t))
##book.save('modele_base_bulle.xls')
##
##
##alpha, sigma2 =estimation_alpha_sigma2(Rp)
##print('alpha: ',alpha)
##print('sigma2: ',sigma2)
























