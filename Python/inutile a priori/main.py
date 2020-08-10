from simulation_Q_base import *
from recuperation_donnees import charger_donnees
from estimation import estimation_alpha_sigma2, IC, estimation_CT
from matplotlib.dates import *
from datetime import *


def Fit_model(begin, end, model):
    d = string_to_database(begin)
    f = string_to_database(end)
    R,P,Q,cours=charger_donnees()
    Rp=R[d:f+1]
    Pp=P[d:f+1]
    Qp=Q[d:f+1]
    Q0=Q[d-1]

    if model == 'baseline':
        a=0.002
        if d > 1500:
            if d > 1600:
                if d > 1700:
                    if d > 1800:
                        if d > 1900:
                            if d > 2500:
                                B_tilde = 1
                            else:
                                B_tilde = 10
                        else:
                            B_tilde = 30
                    else:
                        B_tilde = 1500
                else:
                    B_tilde = 4000
            else:
                B_tilde = 3000
        else:
            B_tilde = 20000
        x0=estimation_a_B_tilde(a,B_tilde,R,Q,d,f)
        a=x0['x'][0]
        B_tilde=x0['x'][1]
        Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
        graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,type=(1,2))
        plot_cours(cours,d,f)

        alpha,sigma2=estimation_alpha_sigma2(Rp)
        intervalle=IC(Rp,0.95)
        print('B_tilde: ',B_tilde,'\n')
        print('parametres annuels\n')

        mu=alpha-0.5*sigma2
        print('mu: ',365*mu)
        print([365*i for i in intervalle[0]])
        print('\nsigma2: ',365*sigma2)
        print([365*i for i in intervalle[1]])
        print('\na: ',a,'\n')
        r = 0.1/365
        print('couts totaux: ',estimation_CT(a,alpha,sigma2,B_tilde,r),'\n')

########################################################################################

# example
Fit_model('2012-11-09', '2014-10-10', 'baseline')        




