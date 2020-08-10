""" module qui sert a simuler Q, estimer les parameters et faire les graphiques
    dans le modele de base """

from numpy import *
from scipy.optimize import minimize, show_options
from matplotlib.pyplot import *
from matplotlib.dates import *
from datebase import *

def simulationQ_step(a,B_tilde,Rp,Q0,step):
    Rt=[144 * r for r in Rp] # revenu journalier
    Rt2=[Rt[i] for i in arange(step-1,len(Rt),step)]
    T2=len(Rt2) # duree de la periode d'etude
    Bt2=B_tilde/exp(step*a*arange(1,T2+1)) # barriere non detrendee
    Q_sim2=[]
    P_sim2=[]
    Q_sim2.append(max(Q0,Rt2[0]/Bt2[0]))
    for t in range(1,T2):
        Q_sim2.append(max(Q_sim2[-1],Rt2[t]/Bt2[t]))
    return Q_sim2,[r/q for r,q in zip(Rt2,Q_sim2)]

def objective_function_step(x,R,Q,d,f,step):

    """ fonction objectif pour l'estimation de a et B_tilde. x est un array
    concatenant a et B_tilde.
    d: debut de la periode d'estimation
    f: fin de la periode d'estimation"""
    a=x[0]
    B_tilde=x[1]
    Q_sim2,P_sim2=simulationQ_step(a,B_tilde,R[d:f+1],Q[d-1],step)
    Qp=Q[d:f+1]
    Qp2=[Qp[i] for i in arange(step-1,f-d+1,step)]
    return sum([(qs-q)**2/q**2 for qs,q in zip(Q_sim2,Qp2)])

def estimation_a_B_tilde_step(a0,B_tilde0,R,Q,d,f,step):

    """ estimation de a et B_tilde en minimisant une distance entre le
    Q simule et le vrai Q. a0 et B_tilde0: points de depart pour l'optimisation.
    Pour les autres arguments, voir ma fonction "objective_function """
    x0=array([a0,B_tilde0])
    res=minimize(objective_function_step, x0, args=(R,Q,d,f,step),\
                 method='Nelder-Mead',options={'xtol': 1e-8, 'disp': False})
    return res

def objective_a_0_step(x,R,Q,d,f,step):

    """ fonction objectif avec a fixe a 0 """
    
    B_tilde=x[0]
    Q_sim2,P_sim2=simulationQ_step(0,B_tilde,R[d:f+1],Q[d-1],step)
    Qp=Q[d:f+1]
    Qp2=[Qp[i] for i in arange(step-1,f-d+1,step)]
    return sum([(qs-q)**2/q**2 for qs,q in zip(Q_sim2,Qp2)])

def estimation_a_0_step(B_tilde0,R,Q,d,f,step):

    """ estimation de B_tilde avec a fixe a 0. """

    x0=array([B_tilde0])
    res=minimize(objective_a_0_step, x0, args=(R,Q,d,f,step),\
                 method='Nelder-Mead',options={'xtol': 1e-8, 'disp': False})
    return res

def graphique_simulation_step(a,B_tilde,Q_sim2,P_sim2,Qp2,Pp2,\
                              d,f,h,step,type=(1,)):

    # h: date du halving
    lw=3 #linewidth
    fg=(6,4)
    ft='xx-large'
    chemin=r'C:\Users\Benjamin\Dropbox\bitcoin\modèle SS\Rédaction'
    
    xdates=[date_base(j) for j in range(d,f+1)]
    xdates2=[xdates[i] for i in arange(step-1,f-d+1,step)]
    if d<1000: # c'est la premiere periode
        periode='1'
    else:
        periode='2'
    
    T2=len(Q_sim2)
    At2=exp(step*a*arange(0,T2))
    for t in type:
        if t==1:
            fig1, ax1 = subplots(figsize=fg)
            ax1.plot(xdates2,log(Qp2),'r',linewidth=lw,label='log Q')
            ax1.plot(xdates2,log(Q_sim2),'b',linewidth=lw,label=r'log $Q^{sim}$')
            ax1.axvline(x=date_base(h),color='k',linestyle='dashed',\
                        linewidth=lw,label='halving')
            gcf().autofmt_xdate()
            ax1.tick_params(axis='both',labelsize=ft)
            ax1.xaxis.set_major_locator(MonthLocator(interval=9))
            legend(fontsize=ft)
            #fig1.savefig(chemin+'\\Q_Q_sim'+periode+'.png')
            #print('graphique Q_Q_sim'+periode+'.png sauvegarde! Chemin= ',\
            #      chemin)
            show()
        if t==2:
            fig2, ax2 = subplots(figsize=(6,5))
            ax2.plot(xdates2,[a*p for a,p in zip(At2,P_sim2)],'b',linewidth=lw,\
                 label=r'$\tilde{P}^{sim}$')
            ax2.plot(xdates2,[a*p for a,p in zip(At2,Pp2)],'g',linewidth=lw,\
                 label=r'$\tilde{P}$')
            ax2.plot(xdates2,T2*[B_tilde],'r',linewidth=lw,\
                 label='detrended barrier')
            ax2.axvline(x=date_base(h),color='k',linestyle='dashed',\
                        linewidth=lw,label='halving')
            gcf().autofmt_xdate()
            ax2.tick_params(axis='both',labelsize=ft)
            ax2.xaxis.set_major_locator(MonthLocator(interval=9))
            if d<1000:
                legend(fontsize=ft)
                gcf().subplots_adjust(left=0.15)
            #fig2.savefig(chemin+'\\P_P_sim'+periode+'.png')
            #print('graphique P_P_sim'+periode+'.png sauvegarde! Chemin= ',\
            #     chemin)
            show()

