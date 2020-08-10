from simulation_Q_base import *
from recuperation_donnees import charger_donnees
from recuperation_donnees import get_exchange_rate_kaiko
from estimation import estimation_alpha_sigma2, IC, estimation_CT

kaiko = get_exchange_rate_kaiko()
R,P,Q,cours=charger_donnees()

lw=3
fg=(12,6)
ft='xx-large'

d = 722
f = len(kaiko)-1

xdates=[date_base(j) for j in range(d,f+1)] # date index -> real dates
fig, ax = subplots(figsize=fg)
##ax.plot(xdates,cours[d:f+1],linewidth=lw,label='our exchange rate')
##ax.plot(xdates,kaiko[d:f+1],linewidth=lw,label='Kaiko exchange rate')
ax.plot(xdates,[log(c) for c in cours[d:f+1]],linewidth=lw,label='Coindesk Dataset')
ax.plot(xdates,[log(c) for c in kaiko[d:f+1]],linestyle='dotted',linewidth=lw,label='Kaiko Dataset')
ax.xaxis.set_major_locator(MonthLocator(interval=9))
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
gcf().autofmt_xdate()
ax.tick_params(axis='both',labelsize=ft)
legend(fontsize=ft)
gcf().subplots_adjust(left=0.15)
ax.margins(0.03)
show()

R = R[:722] + [r*k/c for r,k,c in zip(R[d:f+1],kaiko[d:f+1],cours[d:f+1])]


d=2091 #start date 2091
f=3003 #end date 3003 

r=0.1/365 

a=0.00207
B_tilde=5.3
Rp=R[d:f+1]
Pp=P[d:f+1]
Qp=Q[d:f+1]
Q0=Q[d-1]

x0=estimation_a_B_tilde(a,B_tilde,R,Q,d,f)
a=x0['x'][0]
B_tilde=x0['x'][1]
print('a: ',a)
print('B_tilde: ',B_tilde)

Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)
graphique_simulation(a,B_tilde,Q_sim,P_sim,Qp,Pp,d,f,type=(1,2))
plot_cours(cours,d,f)

alpha,sigma2=estimation_alpha_sigma2(Rp)
intervalle=IC(Rp,0.95)

print('parametres annuels\n')

mu=alpha-0.5*sigma2
print('mu: ',365*mu)
print([365*i for i in intervalle[0]])
print('\nsigma2: ',365*sigma2)
print([365*i for i in intervalle[1]])
print('\na: ',a,'\n')
print('r fixe: ',r,'\n')

print('couts totaux: ',estimation_CT(a,alpha,sigma2,B_tilde,r),'\n')
