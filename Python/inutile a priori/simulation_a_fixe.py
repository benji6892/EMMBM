""" module qui sert a simuler Q, estimer les parameters et faire les graphiques
    dans le modele de base """

from numpy import *
from scipy.optimize import minimize, show_options
from matplotlib.pyplot import *
from matplotlib.dates import *
from datebase import *

def simulationQ(a,B_tilde,Rp,Q0):

    Rt=[144 * r for r in Rp] # revenu journalier
    T=len(Rt) # duree de la periode d'etude
    Bt=B_tilde/exp(a*arange(1,T+1)) # barriere non detrendee
    Q_sim=[]
    P_sim=[]
    Q_sim.append(max(Q0,Rt[0]/Bt[0]))
    for t in range(1,T):
        Q_sim.append(max(Q_sim[-1],Rt[t]/Bt[t]))
    return Q_sim,[r/q for r,q in zip(Rt,Q_sim)]

def objective_function(x,a,R,Q,d,f):

    """ fonction objectif pour l'estimation de a et B_tilde. x est un array
    concatenant a et B_tilde.
    d: debut de la periode d'estimation
    f: fin de la periode d'estimation"""
    
    B_tilde=x[0]
    Q_sim,P_sim=simulationQ(a,B_tilde,R[d:f+1],Q[d-1])
    Qp=Q[d:f+1]
    return sum([(qs-q)**2/q**2 for qs,q in zip(Q_sim,Qp)])

def estimation_a_B_tilde(a,B_tilde0,R,Q,d,f):

    """ estimation de a et B_tilde en minimisant une distance entre le
    Q simule et le vrai Q. a0 et B_tilde0: points de depart pour l'optimisation.
    Pour les autres arguments, voir ma fonction "objective_function """

    x0=array([B_tilde0])
    res=minimize(objective_function, x0, args=(a,R,Q,d,f),\
                 method='Nelder-Mead',options={'xtol': 1e-8, 'disp': False})
    return res

def graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,h,type=(1,)):

    # h: date du halving
    lw=3 #linewidth
    fg=(6,4)
    ft='xx-large'
    chemin=r'C:\Users\Benjamin\Dropbox\bitcoin\modèle SS\Rédaction'
    
    xdates=[date_base(j) for j in range(d,f+1)]
    if d<1000: # c'est la premiere periode
        periode='1'
    else:
        periode='2'
    
    T=len(Q_sim)
    At=exp(a*arange(0,T))
    for t in type:
        if t==1:
            fig1, ax1 = subplots(figsize=fg)
            ax1.plot(xdates,log(Qp),'r',linewidth=lw,label='log Q')
            ax1.plot(xdates,log(Q_sim),'b',linewidth=lw,label=r'log $Q^{sim}$')
            ax1.axvline(x=date_base(h),color='k',linestyle='dashed',\
                        linewidth=lw,label='halving')
            gcf().autofmt_xdate()
            ax1.tick_params(axis='both',labelsize=ft)
            ax1.xaxis.set_major_locator(MonthLocator(interval=9))
            legend(fontsize=ft)
            fig1.savefig(chemin+'\\Q_Q_sim'+periode+'.png')
            print('graphique Q_Q_sim'+periode+'.png sauvegarde! Chemin= ',\
                  chemin)
        if t==2:
            fig2, ax2 = subplots(figsize=(6,5))
            ax2.plot(xdates,[a*p for a,p in zip(At,P_sim)],'b',linewidth=lw,\
                 label=r'$\tilde{P}^{sim}$')
            ax2.plot(xdates,[a*p for a,p in zip(At,Pp)],'g',linewidth=lw,\
                 label=r'$\tilde{P}$')
            ax2.plot(xdates,T*[B_tilde],'r',linewidth=lw,\
                 label='detrended barrier')
            ax2.axvline(x=date_base(h),color='k',linestyle='dashed',\
                        linewidth=lw,label='halving')
            gcf().autofmt_xdate()
            ax2.tick_params(axis='both',labelsize=ft)
            ax2.xaxis.set_major_locator(MonthLocator(interval=9))
            if d<1000:
                legend(fontsize=ft)
                gcf().subplots_adjust(left=0.15)
            fig2.savefig(chemin+'\\P_P_sim'+periode+'.png')
            print('graphique P_P_sim'+periode+'.png sauvegarde! Chemin= ',\
                  chemin)

