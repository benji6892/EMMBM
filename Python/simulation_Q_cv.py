""" module qui sert a simuler Q, estimer les parameters et faire les graphiques
    dans le modele avec cout variable """

from numpy import *
from scipy.optimize import minimize, show_options
from matplotlib.pyplot import *
from matplotlib.dates import *
from datebase import *

def distribution_initiale(a,B_tilde,Q0,C0):

    """ pour simuler la trajectoirede Q on a besoin d'une distribution
    initiale. A priori ce choix a tres peu d'impact. Retourne trois listes:
    celle des couts, celle du hashrate potentielle et celle du hashrate
    effectif. Voir la fonction simulationQ. Q0: hashrate la veille du debut
    de la periode d'etude; C0: cout variable de la nouvelle machine disponible
    la veille du debut de la periode d'etude. """

    # on choisit ici une distibution "en exponentiel"
    Nb=floor(log(B_tilde/C0)/a)+1 # nombre de periodes ou on mine
    q0=Q0*(exp(a)-1)/(exp(a*Nb)-1)
    coeffs=exp(a*arange(0,Nb))
    couts=[B_tilde/c for c in coeffs]
    Q_pot=[q0*c for c in coeffs]
    Q_eff=[q0*c for c in coeffs]
    return couts,Q_pot,Q_eff


def simulationQ_cv(a,B_tilde,Rp,Q0,C0):

    """ fonction qui simule la trajectoire de Q et retourne la trajectoire de
    Q simulee et les prix simules. Rp: R pendant la periode d'etude;
    Q0: hashrate la veille du debut de la periode d'etude;
    C0: cout variable de la nouvelle machine disponible
    la veille du debut de la periode d'etude. """
    
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
    return Q_sim,P_sim

def objective_function_cv(x,R,Q,d,f):

    """ fonction objectif pour l'estimation de a et B_tilde. x est un array
    concatenant a, B_tilde et C0. """
    
    a=x[0]
    B_tilde=x[1]
    C0=x[2]
    #print('a: ',a,'   B_tilde: ',B_tilde,'   C0: ',C0)
    if B_tilde - C0 < 0.01:
        #print('f: ',1000000 + 1000000 * (0.01 + C0 - B_tilde),'\n')
        return 1000000 + 1000000 * (0.01 + C0 - B_tilde)
    elif C0 < 0.001:
        #print('f: ',1000000 + 1000000 * (0.001 - C0),'\n')
        return 1000000 + 1000000 * (0.001 - C0)
    elif a < 0.0001:
        #print('f: ',1000000 + 1000000 * (0.0001 - a),'\n')
        return 1000000 + 1000000 * (0.0001 - a)
    else:
        try:
            Q_sim,P_sim=simulationQ_cv(a,B_tilde,R[d:f+1],Q[d-1],C0)
            Qp=Q[d:f+1]
            #print('f: ',sum([(qs-q)**2/q**2 for qs,q in zip(Q_sim,Qp)]),'\n')
            return sum([(qs-q)**2/q**2 for qs,q in zip(Q_sim,Qp)])
        except IndexError:
            #print('f: ',1000000000,'\n')
            return 1000000000


def estimation_a_B_tilde_C0(a0,B_tilde0,C0,R,Q,d,f):

    """ estimation de a et B_tilde en minimisant une distance entre le
    Q simule et le vrai Q. a0, B_tilde0 et C0: points de depart pour
    l'optimisation. Attention! Cette fonction renvoie directement
    la valeur des parametres. """
    fval=Inf
    x0=array([a0,B_tilde0,C0])
    res=minimize(objective_function_cv, x0, args=(R,Q,d,f),\
                 method='Nelder-Mead',\
                 options={'xtol': 1e-6, 'disp': False, 'maxiter': 500})
    return res['x']


def graphique_simulation_2(a,B_tilde,Q_sim,P_sim,Qp,Pp,Q_sim2,d,f,type=(1,)):

    # h: date du halving
    lw=3 #linewidth
    fg=(6,5)
    ft='xx-large'
    
    xdates=[date_base(j) for j in range(d,f+1)]
    T=len(Q_sim)
    At=exp(a*arange(0,T))
    for t in type:
        if t==1:
            fig1, ax1 = subplots(figsize=fg)
            ax1.plot(xdates,log(Qp),'r',linewidth=lw,label='log Q')
            ax1.plot(xdates,log(Q_sim),'b',linestyle='--',\
                     linewidth=lw,label=r'log $Q^{sim}_{stop}$')
           # ax1.plot(xdates,log(Q_sim2),'g',linestyle='-.',\
        #         linewidth=lw,label=r'log $Q^{sim}_{base}$')
            if (d<1419) and (f>1419):
                ax1.axvline(x=date_base(1419),color='k',linestyle=':',\
                            linewidth=lw,label='halving')
            if (d<2738) and (f>2738):
                ax1.axvline(x=date_base(2738),color='k',linestyle=':',\
                            linewidth=lw,label='halving') 
            gcf().autofmt_xdate()
            ax1.tick_params(axis='both',labelsize=ft)
            ax1.xaxis.set_major_locator(MonthLocator(interval=3))
            legend(fontsize=ft)
            ax1.margins(0.03)
            show()
        if t==2:
            fig2, ax2 = subplots(figsize=fg)
            ax2.plot(xdates,[a*p for a,p in zip(At,P_sim)],'b',linewidth=lw,\
                 linestyle='--',label=r'$\tilde{P}^{sim}_{stop}$')
            ax2.plot(xdates,[a*p for a,p in zip(At,Pp)],'g',linewidth=lw,\
                 label=r'$\tilde{P}$')
            ax2.plot(xdates,T*[B_tilde],'r',linewidth=lw,linestyle='-.',\
                 label='detrended barrier')
            if (d<1419) and (f>1419):
                ax1.axvline(x=date_base(1419),color='k',linestyle=':',\
                            linewidth=lw,label='halving')
            if (d<2738) and (f>2738):
                ax1.axvline(x=date_base(2738),color='k',linestyle=':',\
                            linewidth=lw,label='halving') 
            gcf().autofmt_xdate()
            ax2.tick_params(axis='both',labelsize=ft)
            ax2.xaxis.set_major_locator(MonthLocator(interval=9))
            if d<1000:
                legend(fontsize=ft)
                gcf().subplots_adjust(left=0.15)
            ax2.margins(0.03)
            show()
