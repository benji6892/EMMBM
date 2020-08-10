""" module qui fait du bootstrap sur a et B_tilde_0 dans le modele de base """

from recuperation_donnees import charger_donnees
from simulation_Q_base import *

def chercher_blocs(P,d,f,a0):
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
    
def graphique_blocs(debuts,d,f,P,nb_blocs,B_tilde):
    """ fonction qui plot P/P_tilde avec les blocs """
    lw=3
    P_det=[a*p/B_tilde for a,p in zip(exp(a0*arange(0,f+1-d)),P[d:f+1])]
    plot(range(d,f+1),P_det,linewidth=lw,label='payoff/barrier')
    for i in range(0,nb_blocs):
        axvline(x=debuts[i]+d,color='k',linestyle='dashed',linewidth=lw)
    axhline(y=P_det[0],color='r',linestyle='dashed',linewidth=lw)
    legend()
    show()

def graphiques_bootstrap(a,B_tilde,Rb,Qb,num):
    """ fonction qui plot les graphiques habituels, pour le bootstrap """
    lw=3
    chemin=r'C:\Users\Benjamin\Desktop\graph bootstrap'
    
    At=exp(a*arange(0,len(Rb)))
    x=range(0,len(Rb))
    Pb=[144*r/q for r,q in zip(Rb,Qb)]
    fig,ax=subplots()
    Q_sim,P_sim=simulationQ(a,B_tilde,Rb,Q[d-1])
    plot(x,Qb,'r',linewidth=lw,label='log of observed hashrate')
    plot(x,Q_sim,'b',linewidth=lw,label='log of simulated hashrate')
    legend()
    fig.savefig(chemin+'\\Q'+str(num)+'.png')
    clf()

    fig,ax=subplots()
    plot(x,P_sim,'b',linewidth=lw,\
         label='simulated detrended payoff')
    plot(x,Pb,'g',linewidth=lw,\
         label='observed detrended payoff')
    plot(x,[B_tilde/a for a in At],'r',linewidth=lw,\
         label='detrended barrier ')
    legend()
    fig.savefig(chemin+'\\P'+str(num)+'.png')
    clf()

    fig,ax=subplots()
    plot(x,Rb)
    fig.savefig(chemin+'\\c'+str(num)+'.png')
    clf()

def bootstrap(debuts,d,f,dR,dQ,a0,B_tilde0,num,graph=False):
    """ fonction qui tire un echantillon bootstrap et calibre les parametres """
    fins=[de for de in debuts[1:]]+[f-d]
    nb_blocs=len(debuts)
    sample_array=nb_blocs*random.sample(nb_blocs)
    sample=[int(floor(s)) for s in sample_array]
    dRb=[]
    dQb=[]
    for s in sample:
        dRb+=list(dR[debuts[s]:fins[s]])
        dQb+=list(dQ[debuts[s]:fins[s]])
    Rb=[R[d]]
    Qb=[Q[d]]
    for rb in dRb:
        Rb.append(Rb[-1]*rb)
    for qb in dQb:
        Qb.append(Qb[-1]*qb)
    Rbtot=R[:d]+Rb
    Qbtot=Q[:d]+Qb
    x0=estimation_a_B_tilde(a0,B_tilde0,Rbtot,Qbtot,d,d+len(Rb)-1)
    if x0['x'][0]<0:
        graphiques_bootstrap(x0['x'][0],x0['x'][1],Rb,Qb,num)
    return [x0['x'][0], x0['x'][1]]

def Bootstrap(debuts,d,f,R,Q,a0,B_tilde0,B):
    """ fonction qui fait le bootstrap. Retourne une liate pour a et une liste
    pour B_tilde """
    dR=exp(diff(log(R[d:f+1])))
    dQ=exp(diff(log(Q[d:f+1])))
    vect_a=[]
    vect_B_tilde=[]
    for b in range(0,B):
        print(b)
        res=bootstrap(debuts,d,f,dR,dQ,a0,B_tilde0,b)
        vect_a.append(res[0])
        vect_B_tilde.append(res[1])
    return vect_a,vect_B_tilde
    
random.seed(1)
R,P,Q,cours=charger_donnees()

#*******************************************************************************
#                              1ere periode
#*******************************************************************************

d=812
f=1483

a0=0.0032
B_tilde0=26000

debuts=[0,121,277,417,608] # debuts des blocs [0,182,364,546,728]
#graphique_blocs(debuts,d,f,P,len(debuts),B_tilde0)

B=100
vect_a,vect_B_tilde=Bootstrap(debuts,d,f,R,Q,a0,B_tilde0,B)

print('IC a: ',[percentile(vect_a,2.5),percentile(vect_a,97.5)])
print('IC B_tilde: ',[percentile(vect_B_tilde,5),percentile(vect_B_tilde,95)])

# on en fait un avec un graphique
##dR=exp(diff(log(R[d:f+1])))
##dQ=exp(diff(log(Q[d:f+1])))
##bootstrap(debuts,d,f,dR,dQ,a0,B_tilde0,graph=True)

