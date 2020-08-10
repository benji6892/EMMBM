""" Plots the number of blocks found every day,
the density of the returns of R Vs the N(0,1) density, and shows how Q is
estimated """

from simulation_Q_base import *
from estimation import *
import pickle
from sklearn.linear_model import *
from datebase import *
from matplotlib.pyplot import *

with open('donnees','rb') as fichier:
    mon_depickler=pickle.Unpickler(fichier)
    R=mon_depickler.load()
    P=mon_depickler.load()
    Q=mon_depickler.load()
    cours=mon_depickler.load()

with open('donnees_brutes','rb') as fichier2:
    mon_depickler2=pickle.Unpickler(fichier2)
    N=mon_depickler2.load()
    NB=mon_depickler2.load()
    frais=mon_depickler2.load()
    diff=mon_depickler2.load()
    taille=mon_depickler2.load()


#####*******************************************************************************
#####           graphique avec le nombre de blocs trouve chaque jour
#####*******************************************************************************
##
##lw=3 #linewidth
##fg=(10.8,3.5)
##ft='xx-large'
##
##d=0
### f=3003
##f=3415
##xdates=[date_base(j) for j in range(d,f+1)]
##fig, ax = subplots(figsize=fg)
##ax.plot(xdates,N[d:f+1],'b',linewidth=lw,label='daily number of blocks found')
##ax.plot(xdates,(f+1)*[144-12*1.96],'g',linewidth=lw,label='95% bounds')
##ax.plot(xdates,(f+1)*[144+12*1.96],'g',linewidth=lw)
##ax.axvline(x=date_base(812),color='r',linestyle=':',\
##        linewidth=lw,label='first period')
##ax.axvline(x=date_base(1483),color='r',linestyle=':',\
##        linewidth=lw)
##ax.axvline(x=date_base(2091),ymin=0.27,color='r',linestyle='--',\
##        linewidth=lw,label='second period')
##ax.axvline(x=date_base(3003),color='r',linestyle='--',\
##        linewidth=lw)
##ax.tick_params(axis='both',labelsize=ft)
##ax.set_ylabel('daily number of blocks',fontsize=ft)
##ax.text(date_base(900),350,'1st period',color='red',fontsize=ft)
##ax.text(date_base(2300),350,'2nd period',color='red',fontsize=ft)
##ax.text(date_base(1650),50,'95% confidence bounds',color='green',fontsize=ft)
##gcf().autofmt_xdate()
##ylim(0,400)
##ax.margins(0.03)
##show()
##
###******************************************************************************
###                            test du brownien
###******************************************************************************
##
##def diff(liste):
##    return [e2-e1 for e2,e1 in zip(liste[1:],liste[:-1])]
##
##
##lw=3
##ft='xx-large'
##fg=(10.8,2.7)
##chemin=r'C:\Users\Benjamin\Dropbox\bitcoin\modèle SS\Rédaction'
##
##d=722
##f=3003
##Rp=R[d:f+1]
##trim=0.1
##alpha,sigma2=estimation_alpha_sigma2_tronquee(Rp,trim)
##
##M=diff([log(r) for r in Rp])
###M=(M-alpha-0.5*sigma2)/sqrt(sigma2)
##densite_M=gaussian_kde(M)
##
##N=sorted(M)
##bi=N[int(floor(len(N)*trim/2))]
##bs=N[int(floor(len(N)*(1-trim/2)))-1]
##
###densite theorique
##fun=lambda x: exp(-(x+0.5*sigma2-alpha)**2/(2*sigma2))/sqrt(2*pi*sigma2)
##
##fig, ax = subplots(figsize=fg)
##plage=arange(-5,5,0.01)
##plage=[sqrt(sigma2)*p + alpha-0.5*sigma2 for p in plage]
##ax.plot(plage,densite_M.evaluate(plage),'r',\
##     label='log R',linewidth=lw,linestyle='--')
##ax.plot(plage,fun(array(plage)),'b',linewidth=lw,\
##        label=r'$\mathcal{N}(\mu,\sigma ^2)$')
##ax.tick_params(axis='both',labelsize=ft)
##legend(fontsize=ft)
##ax.margins(0.03)
##show()
##
#####*******************************************************************************
#####                     graphiques pour l'estimation de Q
#####*******************************************************************************
##with open('donnees_brutes', 'rb') as fichier2:
##    mon_depickler2 = pickle.Unpickler(fichier2)
##    N=mon_depickler2.load()
##    Nb=mon_depickler2.load()
##    frais=mon_depickler2.load()
##    diff=mon_depickler2.load()
##
##K=3600*24*10**12
##
### on commence par faire des moyennes la ou on a juste fait la somme
##diff_m=[d/n for d,n in zip(diff,N)] # difficulte par jour
##proba=[1/(a*2**32) for a in diff_m] # proba de trouver un bloc en un hash
##Q_hat=[n/(K*p) for n,p in zip(N,proba)]
##
### variance de l'estimateur de premiere etape
##var=[q/(p*3600*24*10**12) for q,p in zip(Q,proba)]
##bs=[q+1.96*sqrt(v) for q,v in zip(Q,var)]
##bi=[q-1.96*sqrt(v) for q,v in zip(Q,var)]
##
##lw=3 #linewidth
##ft='xx-large'
##fg=(11,5)
##
##d=2500
##f=3003
##lQ=log(Q)
##lQ_hat=log(Q_hat)
##lvar=[v/q**2 for v,q in zip(var,Q)] # variance calculee avec la delta-methode
##lbs=[lq+1.96*sqrt(lv) for lq,lv in zip(lQ,lvar)]
##lbi=[lq-1.96*sqrt(lv) for lq,lv in zip(lQ,lvar)]
##d=2500
##f=3003
##xdates=[date_base(j) for j in range(d,f+1)]
##fig, ax = subplots(figsize=fg)
##ax.plot(xdates,lQ_hat[d:f+1],'b',linewidth=lw,label=r'first step $log(\hat{Q})$')
##ax.plot(xdates,lQ[d:f+1],'r',linewidth=lw,label=r'smoothed $log(\hat{Q})$',\
##        linestyle='--')
##ax.plot(xdates,lbi[d:f+1],'g',linewidth=lw,label='95% confidence bounds',\
##        linestyle='-.')
##ax.plot(xdates,lbs[d:f+1],'g',linewidth=lw,linestyle='-.')
##gcf().autofmt_xdate()
##ax.tick_params(axis='both',labelsize=ft)
##ax.margins(0.03)
##legend(fontsize=ft)
##show()

###*******************************************************************************
###                                 Average fee
###*****************************************************************************

print(mean([100*f/(f+nb) for f, nb in zip(frais[812:1484], NB[812:1484])]))
print(mean([100*f/(f+nb) for f, nb in zip(frais[2091:3004], NB[2091:3004])]))
print(mean([100*f/(f+nb) for f, nb in zip(frais,NB)]))
