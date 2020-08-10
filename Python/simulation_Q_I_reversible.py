from numpy import *
from scipy.optimize import minimize, show_options
from matplotlib.pyplot import *
from matplotlib.dates import *
from datebase import *
from recuperation_donnees import charger_donnees
from simulation_Q_base import simulationQ

def simulationQ_I_reversible(a,C0,Rp):

    Rt=[144 * r for r in Rp] # daily network revenue
    return [(r/C0) * exp(-a*t) for (r,t) in zip(Rt,range(0,len(Rt)))]

def objective_function_I_reversible(x,R,Q,d,f):

    a=x[0]
    C0=x[1]
    Q_sim = simulationQ_I_reversible(a,C0,R[d:f+1])
    Qp=Q[d:f+1]
    return sum([(qs-q)**2/q**2 for qs,q in zip(Q_sim,Qp)])

def estimation_a_C0_I_reversible(a0,C00,R,Q,d,f):

    fval=Inf
    x0=array([a0,C00])
    res=minimize(objective_function_I_reversible, x0, args=(R,Q,d,f),\
                 method='Nelder-Mead',\
                 options={'xtol': 1e-8, 'disp': False, 'maxiter': 1000})
    return res['x']

def graphique_simulation_reversible(Q_sim_rev,Qp,Q_sim_base,d,f):

    # h: date du halving
    lw=3 #linewidth
    fg=(12,6)
    ft='xx-large'
    
    xdates=[date_base(j) for j in range(d,f+1)]

    fig1, ax1 = subplots(figsize=fg)
    ax1.plot(xdates,log(Qp),'r',linewidth=lw,label='log Q')
    ax1.plot(xdates,log(Q_sim_rev),'b',linestyle='--',\
             linewidth=lw,label=r'log $Q^{sim}_{revervible}$')
    ax1.plot(xdates,log(Q_sim_base),'g',linestyle='-.',\
             linewidth=lw,label=r'log $Q^{sim}_{base}$')
    if (d<1419) and (f>1419):
        ax1.axvline(x=date_base(1419),color='k',linestyle=':',\
                    linewidth=lw,label='halving')
    if (d<2738) and (f>2738):
        ax1.axvline(x=date_base(2738),color='k',linestyle=':',\
                    linewidth=lw,label='halving') 
    gcf().autofmt_xdate()
    ax1.tick_params(axis='both',labelsize=ft)
    ax1.xaxis.set_major_locator(MonthLocator(interval=9))
    legend(fontsize=ft)
    ax1.margins(0.03)
    show()


################################################################################

R,P,Q,cours=charger_donnees()

d=812
f=1483
a0=0.003
C00=2767

a,C0 = estimation_a_C0_I_reversible(a0,C00,R,Q,d,f)
Q_sim = simulationQ_I_reversible(a,C0,R[d:f+1])
Q_sim_base = simulationQ(0.0032334, 25996, R[d:f+1], Q[d-1])[0]

graphique_simulation_reversible(Q_sim,Q[d:f+1],Q_sim_base,d,f)

### deuxieme periode
##
##d=2091
##f=3003
##a0=0.001
##C00=60
##
##a,C0 = estimation_a_C0_I_reversible(a0,C00,R,Q,d,f)
##Q_sim = simulationQ_I_reversible(a,C0,R[d:f+1])
##Q_sim_base = simulationQ(0.00207, 5.3, R[d:f+1], Q[d-1])[0]
##
##graphique_simulation_reversible(Q_sim,Q[d:f+1],Q_sim_base,d,f)

