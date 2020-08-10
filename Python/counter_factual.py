""" Counter factual in the model with variable costs. Enables us to change the parameter
value, recompute the new barrier and simulate many GMB trajectories to get the electicity
expenditure / income ratio under the new parameter set. """

from recuperation_donnees import charger_donnees
from estimation import *
from total_electricity_expense import total_elec_expense, total_elec_expense_bis

def Newton_Raphson(f,x1):
    """ Newton-Raphson algorithm with approximated derivative. Finds x such that f(x)=0 """
    eps=0.00001
    x0=x1+1
    while(abs(x1-x0)>eps):
        x0=x1
        f0=f(x0)
        x1=x0-f0*eps/(f(x0+eps)-f0)
    return x1

def simulation_GBM(mu,sigma2,R0,T):
    """ simulates a GMB from date 1 to date T included """
    gauss=random.randn(T)
    gauss=[sqrt(sigma2)*g+mu for g in gauss]
    res=[R0]
    for t in range(0,T):
        res.append(res[-1]*exp(gauss[t]))
    return res

def get_ratio(a,B_tilde,C0,mu,sigma2,R0,Q0,T,nbr_simu):
    """ simulates GMB trajectories and for eahc trajectory, for each day, computes
    the network electricity expenditure / network income ratio """
    random.seed(4) # to be able to reproduce
    trajectoires=[] # stores all the GBM trajectories
    for i in range(0,nbr_simu):
        trajectoires.append(simulation_GBM(mu,sigma2,R0,T))
    conso=[]
    compteur=1
    for t in trajectoires:
        print(compteur)
        compteur+=1
        try:
            Q_sim,P_sim,expense=total_elec_expense(a,B_tilde,t,Q0,C0)
            conso.append(expense)
        except IndexError:
            conso.append(conso[-1])
    ratio=[] # for each trajectory, for each day, stores the ratio of network
    #electricity consumption over network revenue.
    for i in range(0,nbr_simu):
        ratio.append([c/(144*r) for c,r in zip(conso[i],trajectoires[i])])
    return ratio

def get_moyenne(ratio,T,nbr_simu):
    """ for each trajectory, computes the average electricity expenditure / revenue ratio."""
    moyennes=[]
    for i in range(0,nbr_simu):
        moyennes.append(mean(ratio[i][int(T/10):]))
    print(moyennes)
    return mean(moyennes)
      

R,P,Q,cours=charger_donnees()

d=2091
r=0.1/365

T=10000

a=0.00207
C0=0.683
I0=1002

R0=R[d]
Q0=Q[d-1]

alpha=0.001256
sigma2=0.00149
mu=alpha-sigma2/2

B_tilde=5.045 # B_tilde benchmark

nbr_simu=100 # number of simulations

# new value for a parameter
mu=0
#sigma2/=10
#a=0.00095
#I0/=2

# recompute the initial value of the barrier under the new set of parameters.
alpha=mu+0.5*sigma2
B_tilde=Newton_Raphson(lambda b: W0(a,b,C0,alpha,sigma2,r)-I0,5) 
print('nouveau B_tilde: ',B_tilde)

# Maximum number of days a miner can mine
T_max=(1/a)*(log(B_tilde)-log(C0))
print('T_max: ',T_max)

# how much of his exected total income will a miner spend on electricity?
K0=I0+C0*(1-exp(-r*T_max))/r # total cost
print('ratio point de vue mineur: ',1-I0/K0)

# Make simulations to compute the average electricity expenditure / income ratio.
ratio=get_ratio(a,B_tilde,C0,mu,sigma2,R0,Q0,T,nbr_simu)
moyenne=get_moyenne(ratio,T,nbr_simu)
print('moyenne: ',moyenne)
