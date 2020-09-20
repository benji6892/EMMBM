""" plots the descriptive graphs (R, Q) and P detrended with the Moore law."""

from recuperation_donnees import charger_donnees
from simulation_Q_base import *
from matplotlib.dates import *

R,P,Q,cours=charger_donnees()

d=812 # start date 812
f=len(R)-1 # end date 3003

# parameters for a nice graph
lw=3
ft='xx-large'
fg=(10.8,5)

fig, ax1 = subplots(figsize=fg)
xdates=[date_base(j) for j in range(d,f+1)]
s1=log(R[d:f+1])
ax1.plot(xdates,s1,'b',linewidth=lw,label='log Rt',linestyle='--')
ax1.set_ylabel('log Rt',color='b',fontsize=ft)
ax1.tick_params(axis='y',colors='b',labelsize=ft)
ax1.tick_params(axis='x',labelsize=ft)
ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
gcf().autofmt_xdate()

ax2=ax1.twinx()
s2=log(Q[d:f+1])
ax2.plot(xdates,s2,'r',linewidth=lw,label='log Qt')
ax2.set_ylabel('log Qt',color='r',fontsize=ft)
ax2.tick_params(axis='y',colors='r',labelsize=ft)

##fig.tight_layout()
##ax1.margins(0.03)
##ax2.margins(0.03)
##gcf().subplots_adjust(left=0.15, right=0.82)
show()

#a0=0.000959 #Moore law
a0 = 0.0014
xdates=[date_base(j) for j in range(d,f+1)]
P_det=[a*p for a,p in zip(exp(a0*arange(0,f+1-d)),P[d:f+1])]

fig, ax = subplots(figsize=fg)
ax.plot(xdates,log(P_det),linewidth=lw,color='g',label=r'$log(P_t)+at$')
ax.axvline(x=date_base(1550),color='k',linestyle='dashed',linewidth=lw)
ax.axvline(x=date_base(2150),color='k',linestyle='dashed',linewidth=lw)
ax.text(date_base(1000),5,'GPUs',color='k',fontsize=ft)
ax.text(date_base(2800),5,'ASICs',color='k',fontsize=ft)
ax.tick_params(axis='both',labelsize=ft)
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
legend(fontsize=ft)
gcf().autofmt_xdate()
##gcf().subplots_adjust(bottom=0.22,left=0.1)
##ax.margins(0.03)
show()
