""" module qui fait du bootstrap pour estimer tous les parametres du modele.
La procedure est la suivante:

1) A faire une fois pour toutes:
    a) On calcule les rendements de R et de Q, appelés respectivement dR et dQ.
        En effet, comme ces séries ne sont pas stationnaires, utiliser
        la série brute n'a aucun sens.
    b) On détermine les blocs. Pour qu'ils aient du sens, P/barrière doit
        avoir toujours la même valeur au début de chaque bloc. J'ai donc
        retenu la valuer initiale de P/barrière. Par chance, cette valeur
        est celle qui permet de maximiser le nombre de blocs. On en a donc
        5 pour la premiere periode, 7 pour la seconde.
        Voir graphique quand on lance le code.

2) A faire à chaque tirage bootstrap:
    a) On choisit aléatoirement et equiprobablement une liste de blocs (avec
        répétition) de la même taile que le nombre total de blocs.
        (5 pour la première période, 7 pour la seconde).
    b) On forme les séries dR_bootstrap et dQ_bootstrap correspondantes.
    c) En repartant des valeurs initiales de R et de Q, on forme les séries
        R_bootstrap et Q_bootstrap.
    d) On estime le modèle avec ces séries-là et on stocke les paramètres
        estimés.
    e) On recommence 2) autant de fois qu'on veut faire de tirage bootstrap.

Problème qui peut se poser: comment choisir les paramètres initiaux pour
l'optimisation pour chaque tirage bootstrap?
"""



from recuperation_donnees import charger_donnees
from simulation_Q_cv import *
from estimation import *

def chercher_blocs(P,d,f,a0):
    # Maintenant qu'on a les blocs, cette fonction est désormais intuile.
    # Elle est utile seulement pour chercher les blocs.
    """ renvoie une liste qui contient toutes les dates auxquelles
    P_t/P_t_bar est egal a sa valeur initiale """
    P_det=[a*p for a,p in zip(exp(a0*arange(0,f+1-d)),P[d:f+1])]
    sgn=[1*(p-P_det[0]>0) for p in P_det]
    dsgn=diff(sgn)
    dates_possibles=[0]
    for i in range(0,len(dsgn)):
        if not dsgn[i]==0:
            dates_possibles.append(i)
    return dates_possibles
    
def graphique_blocs(debuts,d,f,P,nb_blocs,a0,B_tilde):
    """ fonction qui plot P/P_tilde avec les blocs """
    lw=3
    P_det=[a*p/B_tilde for a,p in zip(exp(a0*arange(0,f+1-d)),P[d:f+1])]
    plot(range(d,f+1),P_det,linewidth=lw,label='payoff/barrier')
    for i in range(0,nb_blocs):
        axvline(x=debuts[i]+d,color='k',linestyle='dashed',linewidth=lw)
    axhline(y=P_det[0],color='r',linestyle='dashed',linewidth=lw)
    legend()
    show()

def graphiques_bootstrap(a,B_tilde,Rb,Qb):
    # Pas super utile. Sert à vérifier qu'on ne fait pas complètement
    # n'importe quoi
    """ fonction qui plot les graphiques habituels, pour le bootstrap """
    lw=3
    At=exp(a*arange(0,len(Rb)))
    x=range(0,len(Rb))
    Pb=[144*r/q for r,q in zip(Rb,Qb)]
    figure(1)
    Q_sim,P_sim=simulationQ(a,B_tilde,Rb,Q[d-1])
    plot(x,Qb,'r',linewidth=lw,label='log of observed hashrate')
    plot(x,Q_sim,'b',linewidth=lw,label='log of simulated hashrate')
    legend()

    figure(2)
    plot(x,[a*p for a,p in zip(At,P_sim)],'b',linewidth=lw,\
         label='simulated detrended payoff')
    plot(x,[a*p for a,p in zip(At,Pb)],'g',linewidth=lw,\
         label='observed detrended payoff')
    plot(x,len(Rb)*[B_tilde],'r',linewidth=lw,\
         label='detrended barrier ')
    legend()
    show()

def bootstrap_cv(debuts,d,f,dR,dQ,a0,B_tilde0,C0,r,graph=False):
    """ fonction qui tire un echantillon bootstrap et calibre les parametres """
    
    # debuts: debuts des blocs
    # d: debut des séries R et Q
    # f: fin des séries R et Q
    # dR: serie des rendements de R
    # dQ: serie des rendements de Q
    # autres parametres: evident.
    
    fins=[de for de in debuts[1:]]+[f-d] # fins des blocs
    nb_blocs=len(debuts)
    sample_array=nb_blocs*random.sample(nb_blocs)
    sample=[int(floor(s)) for s in sample_array] # liste des numeros des blocs.
    dRb=[] # redements de R bootstrap
    dQb=[] # rendements de Q bootstrap
    for s in sample:
        dRb+=list(dR[debuts[s]:fins[s]])
        dQb+=list(dQ[debuts[s]:fins[s]])
    Rb=[R[d]] # R bootstrap initialisé avec valeur initiale
    Qb=[Q[d]] # Q bootstrap initialise avec valeur initiale
    for rb in dRb:
        Rb.append(Rb[-1]*rb)
    for qb in dQb:
        Qb.append(Qb[-1]*qb)
    Rbtot=R[:d]+Rb # on concatene la serie R bootstrap avec toutes les 
                   # vraies valeurs de R qui precedent. Inutile en soi
                   # mais la fonction qui fait l'estimation prend la
                   # serie R complete en parametre.
    Qbtot=Q[:d]+Qb # idem pour Q.
    x0=estimation_a_B_tilde_C0(a0,B_tilde0,C0,Rbtot,Qbtot,d,d+len(Rb)-1)
    a=x0[0]
    B_tilde=x0[1]
    C0=x0[2]
    if graph is True:
        graphiques_bootstrap(a,B_tilde,Rb,Qb)
    alpha,sigma2=estimation_alpha_sigma2(Rb)
    I0=W0(a,B_tilde,C0,alpha,sigma2,r)
    T=(1/a)*(log(B_tilde)-log(C0))
    K0=I0+C0*(1-exp(-r*T))/r
    return [a,alpha-0.5*sigma2,sigma2,B_tilde,I0,C0,T,K0]

def Bootstrap_cv(debuts,d,f,R,Q,a0,B_tilde0,C0,r,B):
    """ fonction qui fait le bootstrap. Retourne une liste pour chacun des
    parametres. """
    dR=exp(diff(log(R[d:f+1]))) # rendements de R
    dQ=exp(diff(log(Q[d:f+1]))) # rendements de Q
    v_a=[]
    v_mu=[]
    v_sigma2=[]
    v_B_tilde=[]
    v_I0=[]
    v_C0=[]
    v_T=[]
    v_K0=[]
    for b in range(0,B):
        print(b)
        res=bootstrap_cv(debuts,d,f,dR,dQ,a0,B_tilde0,C0,r)
        v_a.append(res[0])
        v_mu.append(res[1])
        v_sigma2.append(res[2])
        v_B_tilde.append(res[3])
        v_I0.append(res[4])
        v_C0.append(res[5])
        v_T.append(res[6])
        v_K0.append(res[7])
    return v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0

def IC_bootstrap(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0,conf):
    """ fonction qui affiche les intervalles de confiance pour le niveau demandé """
    print('IC de niveau ',conf,'%\n')
    print('IC a: ',[365*percentile(v_a,(100-conf)/2),\
                365*percentile(v_a,(100+conf)/2)])
    print('IC mu: ',[365*percentile(v_mu,(100-conf)/2),\
          365*percentile(v_mu,(100+conf)/2)])
    print('IC sigma2: ',[365*percentile(v_sigma2,(100-conf)/2),\
          365*percentile(v_sigma2,(100+conf)/2)])
    print('IC B_tilde: ',[percentile(v_B_tilde,(100-conf)/2),\
                percentile(v_B_tilde,(100+conf)/2)])
    print('IC I0: ',[percentile(v_I0,(100-conf)/2),\
          percentile(v_I0,(100+conf)/2)])
    print('IC C0: ',[percentile(v_C0,(100-conf)/2),\
          percentile(v_C0,(100+conf)/2)])
    print('IC T: ',[percentile(v_T,(100-conf)/2),\
          percentile(v_T,(100+conf)/2)])
    print('IC K0: ',[percentile(v_K0,(100-conf)/2),\
          percentile(v_K0,(100+conf)/2)])

def standard_deviation(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0):
    print('\n')
    print('Std a: ',365 * std(v_a))
    print('Std mu: ',365 * std(v_mu))
    print('Std sigma2: ',365 * std(v_sigma2))
    print('Std B_tilde: ',std(v_B_tilde))
    print('Std I0: ',std(v_I0))
    print('Std C0: ',std(v_C0))
    print('Std T: ',std(v_T))
    print('Std K0: ',std(v_K0))
    
random.seed(1)
R,P,Q,cours=charger_donnees()

#*******************************************************************************
#                              1ere periode
#*******************************************************************************

##d=812
##f=1483
##
##a0=0.0032
##B_tilde0=26000
##C0=2767
##r=0.1/365
##
##debuts=[0,121,277,417,608] # debuts des blocs [0,182,364,546,728]
###graphique_blocs(debuts,d,f,P,len(debuts),a0,B_tilde0)
##
##B=100
##v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0=Bootstrap_cv(debuts,\
##                                                            d,f,R,Q,a0,\
##                                                            B_tilde0,C0,r,B)
##
##IC_bootstrap(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0,90)
##IC_bootstrap(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0,95)
##standard_deviation(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0)
##






#*******************************************************************************
#                              2eme periode
#*******************************************************************************

##d=2095
##f=3003
##
##a0=0.00207
##B_tilde0=5.04
##C0=0.683
##r=0.1/365
##
### 2184 2363 2470 2570 2697 2915
##debuts=[0,89,268,375,475,602,820] 
##graphique_blocs(debuts,d,f,P,len(debuts),a0,B_tilde0)
####
##B=100
##v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0=Bootstrap_cv(debuts,\
##                                                            d,f,R,Q,a0,\
##                                                            B_tilde0,C0,r,B)
##IC_bootstrap(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0,90)
##IC_bootstrap(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0,95)
##standard_deviation(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0)
##
##### on en fait un avec un graphique
####dR=exp(diff(log(R[d:f+1])))
####dQ=exp(diff(log(Q[d:f+1])))
####bootstrap_cv(debuts,d,f,dR,dQ,a0,B_tilde0,C0,r,graph=True)


#*******************************************************************************
#                              3eme periode
#*******************************************************************************

d=3369
f=3701

a0=0.00397
B_tilde0=0.545
C0=0.158
r=0.1/365

debuts = [0, 69, 124, 200, 261]
#graphique_blocs(debuts,d,f,P,5,a0,B_tilde0)

####
B=100
v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0=Bootstrap_cv(debuts,\
                                                            d,f,R,Q,a0,\
                                                            B_tilde0,C0,r,B)
IC_bootstrap(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0,90)
IC_bootstrap(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0,95)
standard_deviation(v_a,v_mu,v_sigma2,v_B_tilde,v_I0,v_C0,v_T,v_K0)

                                            

                                            
