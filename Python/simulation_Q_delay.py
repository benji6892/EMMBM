""" In the baseline model, contains functions for simulating Q, estimating
parameters and plotting trajectories for Q and P as well as the exchange rate.
"""

from numpy import *
from scipy.optimize import minimize, show_options
from matplotlib.pyplot import *
from matplotlib.dates import *
from datebase import *

def simulationQdelay(a,B_tilde,delta,Rp,C0):

    Rt=[144 * r for r in Rp] # daily network revenue 
    T=len(Rt) # length of study period
    Bt=B_tilde/exp(a*arange(1,T+1)) # barrier
    C_sim=[]
    Q_sim=[]
    P_sim=[]
    C_sim.append(max(C0,Rt[0]/Bt[0]))
    Q_sim.append(C0)
    for t in range(1,T):
        C_sim.append(max(C_sim[-1],Rt[t]/Bt[t]))
    for t in range(0,abs(int(round(delta)))):
        Q_sim.append(C0)
    for t in range(abs(int(round(delta)))+1,T):    
        Q_sim.append((delta-floor(delta))*C_sim[t-int(ceil(delta))]\
                            +(ceil(delta)-delta)*C_sim[t-int(floor(delta))])
    return C_sim, Q_sim,[r/max(q,0.0001) for r,q in zip(Rt,Q_sim)] # returns simulated Q and P

def objective_function_delay(x,R,Q,d,f):

    """ objective function for the estimation of a, B_tilde and delta.
    x is an array concatenating a, B_tilde and delta.
    Minimizes a distance between the observed trajectory for Q and the
    simulated one.
    d: beginning of estimation period
    f: fend of estimation period """
    
    a=x[0]
    B_tilde=x[1]
    delta=x[2]
    if delta < 0.0001:
        return 1000000 + 1000000 * (0.0001 - delta)
    else:
        C_sim,Q_sim,P_sim=simulationQdelay(a,B_tilde,delta,R[d:f+1],Q[d-1])
        Qp=Q[d:f+1]
        return sum([(qs-q)**2/q**2 for qs,q in zip(Q_sim,Qp)])

def objective_function_payoff_delay(x,R,Q,P,d,f):

    """ objective function for the estimation of a, B_tilde and delta.
    x is an array concatenating a, B_tilde and delta.
    Minimizes a distance between the observed trajectory for P and the
    simulated one.
    d: beginning of estimation period
    f: fend of estimation period """
    
    a=x[0]
    B_tilde=x[1]
    delta=x[2]
    if delta < 0.0001:
        return 1000000 + 1000000 * (0.0001 - delta)
    else:
        C_sim,Q_sim,P_sim=simulationQdelay(a,B_tilde,delta,R[d:f+1],Q[d-1])
        Pp=P[d:f+1]
        '''Use Absolute and not proportional variation'''
        return sum([(ps-p)**2 for ps,p in zip(P_sim,Pp)])

def objective_function_relative_payoff_delay(x,R,Q,P,d,f):

    """ objective function for the estimation of a, B_tilde and delta.
    x is an array concatenating a, B_tilde and delta.
    Minimizes a distance between the observed trajectory for P and the
    simulated one.
    d: beginning of estimation period
    f: fend of estimation period """
    
    a=x[0]
    B_tilde=x[1]
    delta=x[2]
    if delta < 0.0001:
        return 1000000 + 1000000 * (0.0001 - delta)
    else:
        C_sim,Q_sim,P_sim=simulationQdelay(a,B_tilde,delta,R[d:f+1],Q[d-1])
        Pp=P[d:f+1]
        return sum([(ps-p)**2/p**2 for ps,p in zip(P_sim,Pp)])

    
    
def objective_function_payoff_delayfixed(x,delta,R,Q,d,f):

    """ objective function for the estimation of a, B_tilde.
    x is an array concatenating a, B_tilde.
    Minimizes a distance between the observed trajectory for P and the
    simulated one.
    d: beginning of estimation period
    f: fend of estimation period """
    
    a=x[0]
    B_tilde=x[1]
    C_sim,Q_sim,P_sim=simulationQdelay(a,B_tilde,delta,R[d:f+1],Q[d-1])
    Qp=Q[d:f+1]
    return sum([(qs-q)**2/q**2 for qs,q in zip(P_sim,Pp)])

    
def estimation_a_B_tilde_delta(a0,B_tilde0,delta,R,Q,d,f):

    x0=array([a0,B_tilde0,delta])
    res=minimize(objective_function_delay, x0, args=(R,Q,d,f),\
                 method='Nelder-Mead',options={'xtol': 1e-8, 'disp': False})
    return res

def estimation_a_B_tilde_payoff_delay(a0,B_tilde0,delta,R,Q,d,f):

    x0=array([a0,B_tilde0])
    res=minimize(objective_function_payoff_delayfixed, x0, args=(delta,R,Q,d,f),\
                 method='Nelder-Mead',options={'xtol': 1e-8, 'disp': False})
    return res    
    
def estimation_payoff_delay(a0,B_tilde0,delta,R,Q,P,d,f):

    x0=array([a0,B_tilde0,delta])
    res=minimize(objective_function_payoff_delay, x0, args=(R,Q,P,d,f),\
                 method='Nelder-Mead',options={'xtol': 1e-8, 'disp': False})
    return res

def estimation_relative_payoff_delay(a0,B_tilde0,delta,R,Q,P,d,f):

    x0=array([a0,B_tilde0,delta]) 
    res=minimize(objective_function_relative_payoff_delay, x0, args=(R,Q,P,d,f),\
                 method='Nelder-Mead',options={'xtol': 1e-8, 'disp': False})
    return res


def graphique_comparison(a,B_tilde,C_sim,Q_sim):
    
    lw=3 #linewidth
    fg=(13,5)
    ft='xx-large'
    
    xdates=[date_base(j) for j in range(d,f+1)]
    
    T=len(Q_sim)
    At=exp(a*arange(0,T))
    fig, ax = subplots(figsize=fg)
    ax.plot(xdates,log(C_sim),'r',linewidth=lw,label='log C')
    ax.plot(xdates,log(Q_sim),'b',linestyle='--',\
                     linewidth=lw,label=r'log Q')

    gcf().autofmt_xdate()
    ax.tick_params(axis='both',labelsize=ft)
    ax.xaxis.set_major_locator(MonthLocator(interval=9))
    legend(fontsize=ft)
    ax.margins(0.03)
    show()

           

def graphique_simulation_delay(a,B_tilde,delta,Q_sim,P_sim,Qp,Pp,d,f,type=(1,)):

    """ When type = 1, plots Q. When type = 2, plots P."""

    # d: start date
    # f: end date
    # h: halving date

    # parameters for a nice graph
    lw=3 #linewidth
    fg=(12,6)
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
        if t==2:
            fig2, ax2 = subplots(figsize=fg)
            ax2.plot(xdates,P_sim,'b',linewidth=lw,\
                 linestyle='--',label='simulated payoff')
            ax2.plot(xdates,Pp,'g',linewidth=lw,\
                 label='observed payoff')
            ax2.plot(xdates,[B_tilde/a for a in At],'r',linewidth=lw,linestyle='-.',\
                 label='barrier')
            if (d<1419) and (f>1419):
                ax2.axvline(x=date_base(1419),color='k',linestyle=':',\
                            linewidth=lw,label='halving')
            if (d<2738) and (f>2738):
                ax2.axvline(x=date_base(2738),color='k',linestyle=':',\
                            linewidth=lw,label='halving')  
            gcf().autofmt_xdate()
            ax2.tick_params(axis='both',labelsize=ft)
            ax2.xaxis.set_major_locator(MonthLocator(interval=9))
            if d<1000:
                legend(fontsize=ft)
            gcf().subplots_adjust(left=0.15)
            ax2.margins(0.03)

            show()

def plot_cours(cours,d,f):
    # cours:    list containing the exchange rate
    # d:        start date
    # f:        end date

    """ plots the exchange rate """

    # parameters for a nice graph
    lw=3
    fg=(6,5)
    ft='xx-large'


    xdates=[date_base(j) for j in range(d,f+1)] # date index -> real dates
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

