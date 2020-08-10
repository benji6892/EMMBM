""" module qui fait des moindres carres non lineaires """

from numpy import *
from scipy.optimize import minimize, show_options
from simulation_Q_base import simulationQ, graphique_simulation
from recuperation_donnees import charger_donnees
from estimation import estimation_alpha_sigma2, IC, estimation_CT
from matplotlib.pyplot import plot, show

def objective_NLLS(x,R,Q,d,f,step):
    """ fonctino objectif a minimiser """
    a=x[0]
    B_tilde=x[1]
    c=x[2]
    #c=0
    Qp=Q[d:f+1]
    Qp2=[Qp[i] for i in arange(step-1,f-d+1,step)]
    Q0=Q[d-1]
    Rp=R[d:f+1]
    Rt=[144 * r for r in Rp]
    Rt2=[Rt[i] for i in arange(step-1,f-d+1,step)]
    Qp_12=[Q0]+Qp2[:-1]
    v=[(qt-max(qt1,rt-log(B_tilde)+step*a*t)-c)**2 for qt,qt1,rt,t in \
       zip(log(Qp2),log(Qp_12),log(Rt2),range(1,len(Rt2)+1))]
##    v=[abs(qt-max(qt1,rt-log(B_tilde)+a*t)) for qt,qt1,rt,t in \
##       zip(log(Qp2),log(Qp_12),log(Rt2),range(1,len(Rt2)+1))]
    return sum(v)

def get_fitted(x,R,Q,d,f,step):
    """ fonction qui sert a recuperer la serie fittee. Attention! Ce n'est
    pas la serie simulee. A chaque fois on repart du vrai point pour
    simuler le suivant. """
    a=x[0]
    B_tilde=x[1]
    c=x[2]
    #c=0
    Qp=Q[d:f+1]
    Qp2=[Qp[i] for i in arange(step-1,f-d+1,step)]
    Q0=Q[d-1]
    Rp=R[d:f+1]
    Rt=[144 * r for r in Rp]
    Rt2=[Rt[i] for i in arange(step-1,f-d+1,step)]
    Qp_12=[Q0]+Qp2[:-1]
    q_fit=[max(qt1,rt-log(B_tilde)+step*a*t)+c for qt1,rt,t in \
           zip(log(Qp_12),log(Rt2),range(1,len(Rt2)+1))]
    plot(log(Qp_12))
    plot([r-log(B_tilde)+a*step*t for r,t in zip(log(Rt2),range(1,len(Rt2)+1))])
    show()
    return q_fit

def get_errors(Qp,q_fit,step):
    """ fonction qui sert a recuperer les erreurs estimees """
    Qp2=[Qp[i] for i in arange(step-1,f-d+1,step)]
    return [q1-q2 for q1,q2 in zip(log(Qp2),q_fit)]

def estimation_NLLS(a0,B_tilde0,c0,R,Q,d,f,step):

    x0=array([a0,B_tilde0,c0])
    res=minimize(objective_NLLS, x0, args=(R,Q,d,f,step),\
                 method='Nelder-Mead',options={'xtol': 1e-8, 'disp': False})
    return res


def var_covar(a,B_tilde,c,R,Q,d,f,q_fit,step):

    Qp=Q[d:f+1]
    Qp2=[Qp[i] for i in arange(step-1,f-d+1,step)]
    Q0=Q[d-1]
    Rp=R[d:f+1]
    Rt=[144 * r for r in Rp]
    Rt2=[Rt[i] for i in arange(step-1,f-d+1,step)]
    Qp_12=[Q0]+Qp2[:-1]
    T=f+1-d
    T2=len(Rt2)

    ind=[1*(rt-log(B_tilde)+step*a*t>=qt1) for rt,t,qt1 in \
         zip(log(Rt2),range(1,T2+1),log(Qp_12))]
    print(ind)
    errors=[q1-q2 for q1,q2 in zip(log(Qp2),q_fit)]
    proba=mean(ind)
    proba=0.95
    
    ET=(T+1)/2
    ET2=(T+1)*(2*T+1)/6
  
    V=matrix([[B_tilde**2*(ET2-proba*ET**2)/(proba*(1-proba)*(ET2-ET**2)),\
                 B_tilde*ET/(proba*(ET2-ET**2)),B_tilde/(1-proba)],\
                [B_tilde*ET/(proba*(ET2-ET**2)),1/(proba*(ET2-ET**2)),0],\
                [B_tilde/(1-proba),0,1/(1-proba)]])
    m0=mean([i*e**2 for i,e in zip(ind,errors)])
    m1=mean([t*step*i*e**2 for t,i,e in zip(range(1,T2+1),ind,errors)])
    m2=mean([(t*step)**2*i*e**2 for t,i,e in zip(range(1,T2+1),ind,errors)])
    m=mean([e**2 for e in errors])

    m0=mean([e**2 for e in errors])
    m1=mean([t*step*e**2 for t,e in zip(range(1,T2+1),errors)])
    m2=mean([(t*step)**2*e**2 for t,e in zip(range(1,T2+1),errors)])
    
    W=matrix([[m0/B_tilde**2,-m1/B_tilde,-m0/B_tilde],\
              [-m1/B_tilde,m2,m1],[-m0/B_tilde,m1,m]])   
    return V*W*V/T2



if __name__ == "__main__":

    R,P,Q,cours=charger_donnees()

    d=812 #debut 812 et 2091
    f=1483 #fin 1483, 3003 et len(R)-1
    h=2738 #halving  1419 et 2738
    r=0.1/365 

    a=0.0028
    B_tilde=15000
    c=0

    Rp=R[d:f+1]
    Pp=P[d:f+1]
    Qp=Q[d:f+1]
    Q0=Q[d-1]

    step=30
    print('step: ',step,'\n')

    x0=estimation_NLLS(a,B_tilde,c,R,Q,d,f,step)
    a=x0['x'][0]
    B_tilde=x0['x'][1]
    c=x0['x'][2]
    

    q_fit=get_fitted([a,B_tilde,c],R,Q,d,f,step)
    errors=get_errors(Qp,q_fit,step)
##
####    Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
####    graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,h,type=(1,))
##
    Qp2=[Qp[i] for i in arange(step-1,f-d+1,step)]

    var=var_covar(a,B_tilde,c,R,Q,d,f,q_fit,step)
    print('a: ',a,'  (',sqrt(var[1,1]),')')
    print('B0: ',B_tilde,'  (',sqrt(var[0,0]),')')
    print('c: ',c,'  (',sqrt(var[2,2]),')')

####
####    plot(errors,'.')
####    show()


