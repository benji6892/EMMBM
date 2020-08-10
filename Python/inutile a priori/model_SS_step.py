"""Estime le modele de base et trace les graphiques"""

from simulation_Q_step import *
from recuperation_donnees import charger_donnees
from estimation import estimation_alpha_sigma2, IC, estimation_CT

def plot_cours(cours,d,f):

    """ fonction qui trace le cours pour chacune des periodes """
    lw=3
    fg=(6,5)
    ft='xx-large'
    chemin=r'C:\Users\Benjamin\Dropbox\bitcoin\modèle SS\Rédaction'

    xdates=[date_base(j) for j in range(d,f+1)]
    if d<1000: # c'est la premiere periode
        periode='1'
    else:
        periode='2'
    fig, ax = subplots(figsize=fg)
    ax.plot(xdates,cours[d:f+1],linewidth=lw,label='exchange rate')
    ax.xaxis.set_major_locator(MonthLocator(interval=9))
    gcf().autofmt_xdate()
    ax.tick_params(axis='both',labelsize=ft)
    legend(fontsize=ft)
    gcf().subplots_adjust(left=0.15)
    fig.savefig(chemin+'\\cours'+periode+'.png')
    print('graphique cours'+periode+'.png sauvegarde! Chemin= ',chemin)
    

R,P,Q,cours=charger_donnees()

#*******************************************************************************
#                             premiere periode
#*******************************************************************************

##print('\npremiere periode\n')
##
##d=812 #debut 722
##f=1483 #fin
##h=1419 #halving
##r=0.1/365 # facteur d'escompte annuel
##
##a=0.0032334
##B_tilde=25996
##Rp=R[d:f+1]
##Pp=P[d:f+1]
##Qp=Q[d:f+1]
##Q0=Q[d-1]
##
##x0=estimation_a_B_tilde(a,B_tilde,R,Q,d,f)
##a=x0['x'][0]
##B_tilde=x0['x'][1]
##
##Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
##graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,h,type=(1,2))
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
##print('\na: ',365*a,'\n')
##print('r fixe: ',r,'\n')
##
##print('couts totaux: ',estimation_CT(a,alpha,sigma2,B_tilde,r),'\n')

###*******************************************************************************
###                             deuxieme periode
###*******************************************************************************



d=2091 #debut
f=3003 #fin 3003
h=2738 #halving
r=0.1/365 

a=0.00207
B_tilde=5.3
Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]

step=10

x0=estimation_a_B_tilde_step(a,B_tilde,R,Q,d,f,step)
a=x0['x'][0]
B_tilde=x0['x'][1]
print('step: ',step)
print('a: ',a)
print('B_tilde: ',B_tilde)

step2=30

Qp2=[Qp[i] for i in arange(step2-1,f-d+1,step2)]
Pp2=[Pp[i] for i in arange(step2-1,f-d+1,step2)]

Q_sim2,P_sim2=simulationQ_step(a,B_tilde,Rp,Q0,step2)
graphique_simulation_step(a,B_tilde,Q_sim2,P_sim2,Qp2,Pp2,d,f,h,step2,type=(1,2))
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
##print('\na: ',365*a,'\n')
##print('r fixe: ',r,'\n')
##
##print('couts totaux: ',estimation_CT(a,alpha,sigma2,B_tilde,r),'\n')
##

##plot([q1-q2 for q1,q2 in zip(log(Q_sim),log(Qp))],'.')
##show()



























