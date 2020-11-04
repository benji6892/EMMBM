from numpy import diff, log, exp, arange
from math import sqrt, floor
from matplotlib.pyplot import subplots, gcf, legend, show, xticks, yticks
from scipy.integrate import quad
from scipy.stats import norm

from model import Model
from util import compute_barrier, compute_P

variable_costs_model_initial_parameters = dict()
variable_costs_model_initial_parameters['1'] = [0.00316, 23858, 2767]
variable_costs_model_initial_parameters['2'] = [0.00207, 5.04, 0.683]


def simulationQ(parameters, R, Q0):

    def initial_distribution(a,B_tilde,Q0,C0):
        Nb=floor(log(B_tilde/C0)/a)+1 
        q0=Q0*(exp(a)-1)/(exp(a*Nb)-1)
        coeffs=exp(a*arange(0,Nb))
        couts=[B_tilde/c for c in coeffs]
        Q_pot=[q0*c for c in coeffs]
        Q_eff=[q0*c for c in coeffs]
        return couts,Q_pot,Q_eff
    

    a = parameters[0]
    B_tilde = parameters[1]
    C0 = parameters[2]
    T=len(R) 
    Bt=B_tilde/exp(a*arange(1,T+1)) 
    Ct=C0/exp(a*arange(1,T+1)) 

    couts,Q_pot,Q_eff=initial_distribution(a,B_tilde,Q0,C0)

    Q_prov=Q0 
    Q_sim=[]
    P_sim=[]
    miner_marg=0 
    next_miner=-1 
    for t in range(0,T):
        barriere=Bt[t]
        reward=R[t]
        if couts[0] > barriere: 
            Q_prov-=Q_eff[0] 
            del couts[0]
            del Q_eff[0]
            del Q_pot[0]
            miner_marg=max(0,miner_marg-1)
            next_miner=max(-1,next_miner-1)
        diff=1 
        P_prov=reward/Q_prov 
        if next_miner > -1:
            critere_entrees=couts[next_miner]
        else:
            critere_entrees=barriere
        if critere_entrees < P_prov: 
            while couts[next_miner] < P_prov and next_miner > -1:
                Q_prov2=Q_prov+Q_pot[next_miner]-Q_eff[next_miner]
                P_prov2=reward/Q_prov2
                if couts[next_miner] < P_prov2: 
                    P_prov=P_prov2
                    Q_prov=Q_prov2
                    Q_eff[next_miner]=Q_pot[next_miner]
                    next_miner-=1
                else: 
                    P_prov=couts[next_miner]
                    Q_eff[next_miner]+=reward/P_prov-Q_prov
                    diff=0 
            if next_miner == -1 and barriere < P_prov:
                P_prov=barriere
                couts.append(Ct[t])
                Q_eff.append(reward/P_prov-Q_prov)
                Q_pot.append(reward/P_prov-Q_prov)
            miner_marg=next_miner+diff
        elif P_prov < couts[miner_marg]:
            while couts[miner_marg] > P_prov:
                Q_prov2=Q_prov-Q_eff[miner_marg]
                P_prov2=reward/Q_prov2
                if couts[miner_marg] > P_prov2: 
                    P_prov=P_prov2
                    Q_prov=Q_prov2
                    Q_eff[miner_marg]=0
                    miner_marg+=1
                else: 
                    P_prov=couts[miner_marg]
                    Q_eff[miner_marg]+=reward/P_prov-Q_prov
                    diff=0
            next_miner=miner_marg-diff
        Q_sim.append(reward/P_prov)
        P_sim.append(P_prov)
        Q_prov=Q_sim[-1]
    return Q_sim


def objective_function(parameters, R, Q, P, Q_initial):
    a = parameters[0]
    B_tilde = parameters[1]
    C0 = parameters[2]
    if B_tilde - C0 < 0.01:
        return 1000000 + 1000000 * (0.01 + C0 - B_tilde)
    elif C0 < 0.001:
        return 1000000 + 1000000 * (0.001 - C0)
    elif a < 0.0001:
        return 1000000 + 1000000 * (0.0001 - a)
    else:
        try:
            Q_sim = simulationQ(parameters, R, Q_initial)
            return sum([(qs-q)**2/q**2 for qs,q in zip(Q_sim,Q)])
        except IndexError:
            return 1000000000


def total_costs(parameters, trend_brownian, var_brownian, interest_rate):

    a = parameters[0]
    B_tilde = parameters[1]
    C0 = parameters[2]
    alpha = trend_brownian
    sigma2 = var_brownian
    r = interest_rate

    def densite_Ps(x,s,a,B_tilde,alpha,sigma2):
        deno=sqrt(sigma2*s)
        A=(1/deno)*norm.pdf((log(B_tilde)-log(x)+(alpha-0.5*sigma2)*s)/deno)
        B=exp((log(B_tilde)-log(x)-a*s)*(1-2*((a+alpha)/sigma2)))
        C=(2*((a+alpha)/sigma2)-1)*\
           norm.cdf((log(x)-log(B_tilde)+(2*a+alpha-0.5*sigma2)*s)/deno)
        D=(1/deno)*norm.pdf((log(x)-log(B_tilde)+(2*a+alpha-0.5*sigma2)*s)/deno)
        return (1/x)*(A+B*(C+D))


    def esp_profit_cv(s,a,B_tilde,C0,alpha,sigma2):
        integral = quad(lambda x: (x-C0)*densite_Ps(x,s,a,B_tilde,alpha,sigma2),\
             C0, B_tilde*exp(-a*s),epsrel=0.01)
        return integral[0]

    def W0(a,B_tilde,C0,alpha,sigma2,r):
        T=(1/a)*(log(B_tilde)-log(C0))
        integral = quad(lambda s: esp_profit_cv(s,a,B_tilde,\
                                                C0,alpha,sigma2)*exp(-r*s),0, T,\
                        epsrel=0.01)
        return integral[0]

    I0=W0(a,B_tilde,C0,alpha,sigma2,r)
    print('Price of mining rig: ',I0)
    T=(1/a)*(log(B_tilde)-log(C0))
    print('max life time minig rig: ' ,T/365)
    return I0+C0*(1-exp(-r*T))/r
    
parameters_description = []
parameters_description.append({'name': 'rate of technical progress', 'multiply_by': 365})
parameters_description.append({'name': 'barrier_initial_value'})
parameters_description.append({'name': 'initial electricity cost per Th/s'})
variable_costs_model = Model('model with variable costs', parameters_description, simulationQ,\
                             total_costs, objective_function=objective_function)


