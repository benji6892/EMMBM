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
from simulation_Q_delay import *
from estimation import *

def bootstrap(debuts,d,f,dR,dQ,a0,B_tilde0,delta_0,r):
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
    Pbtot = [144 * r/q for r,q in zip(Rbtot,Qbtot)]
    x0=estimation_payoff_delay(a0,B_tilde0,delta_0,Rbtot,Qbtot,Pbtot,d,d+len(Rb)-1)
    a=max(x0['x'][0],0) # a negatif n'a pas vraiment de sens.
    B_tilde=x0['x'][1]
    delta=x0['x'][2]
    alpha,sigma2=estimation_alpha_sigma2(Rb)
    CT=estimation_CT_delay(a,delta,alpha,sigma2,B_tilde,r) # couts totaux
    return [a,B_tilde,delta,CT]

def Bootstrap(debuts,d,f,R,Q,a0,B_tilde0,delta_0,r,B):
    """ fonction qui fait le bootstrap. Retourne une liste pour chacun des
    parametres. """
    dR=exp(diff(log(R[d:f+1]))) # rendements de R
    dQ=exp(diff(log(Q[d:f+1]))) # rendements de Q
    v_a=[]
    v_B_tilde=[]
    v_delta=[]
    v_CT=[]  
    for b in range(0,B):
        print(b)
        res=bootstrap(debuts,d,f,dR,dQ,a0,B_tilde0,delta_0,r)
        v_a.append(res[0])
        v_B_tilde.append(res[1])
        v_delta.append(res[2])
        v_CT.append(res[3])
    return v_a,v_B_tilde,v_delta,v_CT

def IC_bootstrap(v_a,v_B_tilde,v_delta,v_CT,conf):
    """ fonction qui affiche les intervalles de confiance pour le niveau demandé """
    print('IC de niveau ',conf,'%\n')
    print('IC a: ',[365*percentile(v_a,(100-conf)/2),\
                365*percentile(v_a,(100+conf)/2)])
    print('IC B_tilde: ',[percentile(v_B_tilde,(100-conf)/2),\
                percentile(v_B_tilde,(100+conf)/2)])
    print('IC delta: ',[percentile(v_delta,(100-conf)/2),\
                percentile(v_delta,(100+conf)/2)])
    print('IC couts totaux: ',[percentile(v_CT,(100-conf)/2),\
          percentile(v_CT,(100+conf)/2)])

def standard_deviation(v_a,v_B_tilde,v_delta,v_CT):
    print('\n')
    print('Std a: ',365 * std(v_a))
    print('Std B_tilde: ',std(v_B_tilde))
    print('Std delta: ',std(v_delta))
    print('Std couts totaux: ',std(v_CT))
    
random.seed(1)
R,P,Q,cours=charger_donnees()

#*******************************************************************************
#                              1ere periode
#*******************************************************************************

##d=812
##f=1483
##
##a0=0.003
##B_tilde0=21963
##delta_0 = 11.5
##
##r=0.1/365
##
##debuts=[0,121,277,417,608] # debuts des blocs [0,182,364,546,728]
###graphique_blocs(debuts,d,f,P,len(debuts),a0,B_tilde0)
##
##B=100
##v_a,v_B_tilde,v_delta,v_CT=Bootstrap(debuts,d,f,R,Q,a0,B_tilde0,delta_0,r,B)
####IC_bootstrap(v_a,v_mu,v_sigma2,v_CT,v_B_tilde,90)
####IC_bootstrap(v_a,v_mu,v_sigma2,v_CT,v_B_tilde,95)
##
##standard_deviation(v_a,v_B_tilde,v_delta,v_CT)
##
### on en fait un avec un graphique
####dR=exp(diff(log(R[d:f+1])))
####dQ=exp(diff(log(Q[d:f+1])))
####bootstrap(debuts,d,f,dR,dQ,a0,B_tilde0,r,CT0,graph=True)





#*******************************************************************************
#                              2eme periode
#*******************************************************************************

##d=2095
##f=3003
##
##a0=0.002475
##B_tilde0=5.100
##delta_0 = 46.5
##r=0.1/365
##
##debuts=[0,89,268,375,475,602,820]
##
##B=100
##v_a,v_B_tilde,v_delta,v_CT=Bootstrap(debuts,d,f,R,Q,a0,B_tilde0,delta_0,r,B)
####IC_bootstrap(v_a,v_mu,v_sigma2,v_CT,v_B_tilde,90)
####IC_bootstrap(v_a,v_mu,v_sigma2,v_CT,v_B_tilde,95)
##
##standard_deviation(v_a,v_B_tilde,v_delta,v_CT)
##
### on en fait un avec un graphique
####dR=exp(diff(log(R[d:f+1])))
####dQ=exp(diff(log(Q[d:f+1])))
####bootstrap(debuts,d,f,dR,dQ,a0,B_tilde0,r,CT0,graph=True)


#*******************************************************************************
#                              3rd period
#*******************************************************************************

d=3491
f=4271

a0=0.00178
B_tilde0=0.5
delta_0 = 42.5
r=0.1/365

debuts=[0, 243, 449, 588, 712]

B=100
v_a,v_B_tilde,v_delta,v_CT=Bootstrap(debuts,d,f,R,Q,a0,B_tilde0,delta_0,r,B)
##IC_bootstrap(v_a,v_mu,v_sigma2,v_CT,v_B_tilde,90)
##IC_bootstrap(v_a,v_mu,v_sigma2,v_CT,v_B_tilde,95)

standard_deviation(v_a,v_B_tilde,v_delta,v_CT)

# on en fait un avec un graphique
##dR=exp(diff(log(R[d:f+1])))
##dQ=exp(diff(log(Q[d:f+1])))
##bootstrap(debuts,d,f,dR,dQ,a0,B_tilde0,r,CT0,graph=True)
                                            
