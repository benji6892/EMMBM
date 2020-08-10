""" Plots the graphs used to explain the model. For the baseline,
idealized P and Q series and a graph to explain mothballing """

from recuperation_donnees import charger_donnees
from simulation_Q_base import *

R,P,Q,cours=charger_donnees()

###############################################################################
#.............................. baseline model ...............................#
###############################################################################



# parameters for nice graphs
lw=3
fg=(10.8,2.7)
ft='xx-large'
    
d=2091 # start date
f=3003 # end date

# let simulate the hashrate in the baseline model
Rp=R[d:f+1]
Q0=Q[d-1]
a0=0.002391
B_tilde0=5.27
x0=estimation_a_B_tilde(a0,B_tilde0,R,Q,d,f)
a=x0['x'][0]
B_tilde=x0['x'][1]
Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)

xdates=[date_base(j) for j in range(d,f+1)]
Bt=[B_tilde]# the barrier
for i in range(1,f-d+1):
    Bt.append(B_tilde*exp(-a*i))


fig, ax =subplots(figsize=fg)
ax.plot(xdates,Bt,'r',linewidth=lw,label='barrier',linestyle='dashed')
ax.plot(xdates,P_sim,'g',linewidth=lw,label='payoff')
gcf().autofmt_xdate()
legend(fontsize=ft)
ax.set_xlabel('time',fontsize=ft)
xticks([])
yticks([])
ax.margins(0.03)
show()

fig, ax = subplots(figsize=fg)
ax.plot(xdates,log(Q_sim),'b',linewidth=lw,label='computing power')
gcf().autofmt_xdate()
legend(fontsize=ft)
ax.set_xlabel('time',fontsize=ft)
xticks([])
yticks([])
ax.margins(0.03)
show()

###############################################################################
#...................... model with mothballing ...............................#
###############################################################################

lw=3
fg=(10.8,5)
ft='xx-large'

d=2091
f=2500

# we still simulate the hashrate in the baseline model because it is just an
# example.
Rp=R[d:f+1]
Q0=Q[d-1]
a0=0.002391
B_tilde0=5.27
x0=estimation_a_B_tilde(a0,B_tilde0,R,Q,d,f)
a=x0['x'][0]
B_tilde=x0['x'][1]
Q_sim,P_sim=simulationQ(a,B_tilde,Rp,Q0)

xdates=[date_base(j) for j in range(d,f+1)]
Bt=[B_tilde]# la barriere
for i in range(1,f-d+1):
    Bt.append(B_tilde*exp(-a*i))


fig, ax =subplots(figsize=fg)
ax.plot(xdates,Bt,'r',linewidth=lw,label='barrier',linestyle='dashed')
ax.plot(xdates,P_sim,'g',linewidth=lw,label='payoff')
ax.plot(xdates,(f+1-d)*[2.7],'b',linewidth=lw,linestyle=':',\
        label='electricity cost')
gcf().autofmt_xdate()
legend(fontsize=ft)
ax.set_xlabel('time',fontsize=ft)
xticks([])
yticks([])
ax.margins(0.03)
show()


