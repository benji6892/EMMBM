""" Module qui realise les tests out of sample. On estime le modele
sur une periode de test seulement et on l'evalue sur toute la periode. """

from recuperation_donnees import charger_donnees
from simulation_Q_base import *
from scipy.stats import *
from matplotlib.dates import *


def erreur(a0,B_tilde0,R,Q,d,F,f):

    """ fonction qui calcule l'erreur commise sur toute la periode,
    y compris la periode de fit """
    # F: fin de l'echantillon d'apprentissage
    
    x0=estimation_a_B_tilde(a0,B_tilde0,R,Q,d,F)
    a=x0['x'][0]
    B_tilde=x0['x'][1]
    Q_sim,P_sim=simulationQ(a,B_tilde,R[d:f+1],Q[d-1])
    return a,B_tilde,sum([(qs-q)**2/q**2 for qs,q in zip(Q_sim,Q[d:f+1])])


def graphique_simulation_test(Q_sim,Qp,d,f,F):

    # F: fin echantillon apprentissage
    lw=3 #linewidth
    ft='xx-large'
    fg=(10.8,6)
    chemin=r'C:\Users\Benjamin\Dropbox\bitcoin\modèle SS\Rédaction'
    
    xdates=[date_base(j) for j in range(d,f+1)]
    fig, ax = subplots(figsize=fg)
    ax.plot(xdates,Qp,'r',linewidth=lw,label='log Q')
    plot(xdates,Q_sim,'b',linewidth=lw,label=r'log $Q^{sim}$',linestyle='--')
    ax.xaxis.set_major_locator(MonthLocator(interval=9))
    ax.axvline(x=date_base(F),color='k',linestyle=':',\
    linewidth=lw,label='end of fit period')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    gcf().autofmt_xdate()
    legend(fontsize=ft)
    gcf().subplots_adjust(bottom=0.25)
    ax.tick_params(axis='both',labelsize=ft)
##    fig.savefig(chemin+'\\out_of_sample_test.png')
##    print('graphique out_of_sample_test.png sauvegarde! Chemin= ',chemin)
    show()


R,P,Q,cours=charger_donnees()


#*******************************************************************************
#                             premiere periode
#*******************************************************************************

##d=812 #debut
##f=1483 #fin
##h=1419
##F=1000 # fin periode d'apprentissage (la pous courte)
##
##a0=0.0032334
##B_tilde0=25996
##Rp=R[d:f+1]
##Pp=P[d:f+1]
##Qp=Q[d:f+1]
##Q0=Q[d-1]
##
##x0=estimation_a_B_tilde(a0,B_tilde0,R,Q,d,F)
##a=x0['x'][0]
##B_tilde=x0['x'][1]
##
##Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
##graphique_simulation_test(log(Q_sim),log(Qp),d,f,F)
##graphique_simulation(Q_sim,P_sim,Qp,Pp,d,f,F,type=(1,2))
##
##
####erreurs=[]
####vect_a=[]
####vect_B_tilde=[]
####for F in arange(1000,f,10):
####    print('F: ',F)
####    a,B_tilde,err=erreur(a0,B_tilde0,R,Q,d,F,f)
####    vect_a.append(a)
####    vect_B_tilde.append(B_tilde)
####    erreurs.append(err)
####
####densite=gaussian_kde(erreurs)
####m=min(erreurs)-1
####M=max(erreurs)+1
####plot(arange(m,M,(M-m)/100),densite.evaluate(arange(m,M,(M-m)/100)))
####show()



#*******************************************************************************
#                             deuxieme periode
#*******************************************************************************


d=2091 #debut
f=3003 #fin
F=2287 # fin periode d'apprentissage (la pous courte)

a0=0.0024054
B_tilde0=5.32
Rp=R[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]

x0=estimation_a_B_tilde(a0,B_tilde0,R,Q,d,F)
a=x0['x'][0]
B_tilde=x0['x'][1]

Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
graphique_simulation_test(log(Q_sim),log(Qp),d,f,F)


##erreurs=[]
##vect_a=[]
##vect_B_tilde=[]
##for F in arange(2395,f,10):
##    print('F: ',F)
##    a,B_tilde,err=erreur(a0,B_tilde0,R,Q,d,F,f)
##    vect_a.append(a)
##    vect_B_tilde.append(B_tilde)
##    erreurs.append(err)
##
##densite=gaussian_kde(erreurs)
##m=min(erreurs)-1
##M=max(erreurs)+1
##plot(arange(m,M,(M-m)/100),densite.evaluate(arange(m,M,(M-m)/100)))
##show()































