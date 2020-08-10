"""Estime le modele de base et trace les graphiques"""

from numpy import *
from datebase import *
from matplotlib.pyplot import *
from matplotlib.dates import *
from simulation_Q_base import simulationQ
from simulation_Q_cv import distribution_initiale, simulationQ_cv
from recuperation_donnees import charger_donnees
from estimation import estimation_alpha_sigma2, IC, estimation_CT

def plot_cours(cours,d,f):

    """ fonction qui trace le cours pour chacune des periodes """
    lw=3
    fg=(13,5)
    ft='xx-large'
    xdates=[date_base(j) for j in range(d,f+1)]
    fig, ax = subplots(figsize=fg)
    ax.plot(xdates,cours[d:f+1],linewidth=lw,label='exchange rate')
    ax.xaxis.set_major_locator(MonthLocator(interval=9))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    gcf().autofmt_xdate()
    ax.tick_params(axis='both',labelsize=ft)
    legend(fontsize=ft)
    gcf().subplots_adjust(left=0.15)
    ax.margins(0.03)
    show()


def graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,type=(1,)):

    lw=3 #linewidth
    fg=(13,5)
    ft='xx-large'
    
    xdates=[date_base(j) for j in range(d,f+1)]
    
    T=len(Q_sim)
    At=exp(a*arange(0,T))
    for t in type:
        if t==1:
            fig1, ax1 = subplots(figsize=fg)
            ax1.plot(xdates,log(Qp),'r',linewidth=lw,label='log Q')
            ax1.plot(xdates,log(Q_sim),'b',linestyle='--',\
                     linewidth=lw,label=r'log $Q^{sim}$')
            gcf().autofmt_xdate()
            ax1.tick_params(axis='both',labelsize=ft)
            ax1.xaxis.set_major_locator(MonthLocator(interval=9))
            legend(fontsize=ft)
            ax1.margins(0.03)
            show()
        if t==2:
            fig2, ax2 = subplots(figsize=fg)
            ax2.plot(xdates,[a*p for a,p in zip(At,Pp)],'g',linewidth=lw,\
                 label=r'$\tilde{P}$')
            ax2.plot(xdates,T*[B_tilde],'r',linewidth=lw,linestyle='-.',\
                 label='detrended barrier')
            gcf().autofmt_xdate()
            ax2.tick_params(axis='both',labelsize=ft)
            ax2.xaxis.set_major_locator(MonthLocator(interval=9))
            ax2.margins(0.03)
            legend(fontsize=ft)
            show()
            

R,P,Q,cours=charger_donnees()

d=2091 #debut 2091
f=len(R)-1 #fin 3003

plot_cours(cours,d,f)

a=0.00207 # Moore law: a=0.00095 # 2ème periode: a=0.00207
B_tilde=5.3/exp(0.00207*(d-2091))

print('B_tilde: ',B_tilde)

C0=0.683/exp(0.00207*(d-2091))
Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]

Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,type=(1,2))






























