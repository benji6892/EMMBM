from recuperation_donnees import charger_donnees
from numpy import *
from scipy.optimize import minimize, show_options
from matplotlib.pyplot import *
from matplotlib.dates import *
from datebase import *
from simulation_Q_cv import distribution_initiale

def total_elec_expense(a,B_tilde,Rp,Q0,C0):

    """ Siulates the trajectory for Q in the model with mothballing and
and computes for each day the network electricity expenditure, using the known
distribution of vintages. """
    
    Rt=[144 * r for r in Rp] # revenu journalier
    T=len(Rt) # duree de la periode d'etude
    Bt=B_tilde/exp(a*arange(1,T+1)) # barriere non detrendee
    Ct=C0/exp(a*arange(1,T+1)) # couts variables des nouvelles machines

    # distributcion initiale
    couts,Q_pot,Q_eff=distribution_initiale(a,B_tilde,Q0,C0)

    # on cree trois vecteurs: un (couts) qui contient les couts variables
    # un (Q_pot) qui contient, pour chaque cout variable, le nombre de mineurs
    # potentiels, c'est a dire deja rentres une fois
    # et le dernier (Q_eff) qui contient, pour chaque cout, le nombre de mineurs
    # qui minent effectivement.
    # Ces trois vecteurs evoluent dans le temps.

    Q_prov=Q0 # hashrate provisoire (avant ajustement par entrees et sorties)
    Q_sim=[]
    P_sim=[]
    expense=[]
    miner_marg=0 # indice de ou se place le mineur (qui mine) le moins
    # performant dans le vecteur des couts
    next_miner=-1 # incide de ou se place le mineur (qui ne mine pas) le plus
    # performant dans le vecteur des couts. -1 veut dire que tous les
    # mineurs potentiels minent
    for t in range(0,T):
        barriere=Bt[t]
        reward=Rt[t]
        # on commence par enlever des vecteurs les mineurs dont le cout
        # variable serait superieur a la barriere
        if couts[0] > barriere: # cela arrive une fois au plus par iteration
            Q_prov-=Q_eff[0] 
            del couts[0]
            del Q_eff[0]
            del Q_pot[0]
            miner_marg=max(0,miner_marg-1)
            next_miner=max(-1,next_miner-1)
        diff=1 # difference entre next_miner et miner_marg
        P_prov=reward/Q_prov # prix provisoire (avant ajustement par entrees
        # et sorties)
        if next_miner > -1:
            critere_entrees=couts[next_miner]
        else:
            critere_entrees=barriere
        if critere_entrees < P_prov: # entrees
            while couts[next_miner] < P_prov and next_miner > -1:
                # ca marche de faire comme ca car couts[-1] est toujours defini 
                Q_prov2=Q_prov+Q_pot[next_miner]-Q_eff[next_miner]
                # on definit un deuxieme hashrate et un deuxieme prix provisoires
                # et on regarde si on a fait entrer trop de monde en faisant
                # entrer tous les mineurs qui ont le cout marginal du plus
                # performant pas encore rentre
                P_prov2=reward/Q_prov2
                if couts[next_miner] < P_prov2: # on n'est pas alles trop loin en
                    # incluant tous les mineurs qui ont ce cout variable
                    P_prov=P_prov2
                    Q_prov=Q_prov2
                    Q_eff[next_miner]=Q_pot[next_miner]
                    next_miner-=1
                else: # on est alles trop loin
                    P_prov=couts[next_miner]
                    Q_eff[next_miner]+=reward/P_prov-Q_prov
                    diff=0 # seul cas ou miner_marg = next_miner
            if next_miner == -1 and barriere < P_prov: # nouvelles entrees
                P_prov=barriere
                couts.append(Ct[t])
                Q_eff.append(reward/P_prov-Q_prov)
                Q_pot.append(reward/P_prov-Q_prov)
            miner_marg=next_miner+diff
        elif P_prov < couts[miner_marg]: # sorties
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
        # il peut y avoir ni entrees ni sorties si
        # couts[miner_marg] < P_prov < couts[next_miner]
        # faire un dessin pour s'en convaincre...
        Q_sim.append(reward/P_prov)
        P_sim.append(P_prov)
        Q_prov=Q_sim[-1]
        expense.append(sum([c*q for c,q in zip(couts,Q_eff)]))
    return Q_sim,P_sim,expense
