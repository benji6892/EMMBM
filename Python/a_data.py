""" plots the price and energy consumption of new machines against time
and estimates the corresponding technical progress rates with
linear regression. """

from datebase import *
from matplotlib.pyplot import *
from numpy import *

#asics = 11*{}
asics=[{},{},{},{},{},{},{},{},{},{},{}]

asics[0]['name']='Bitmain S1'
asics[0]['date']=date(year=2013,month=12,day=1)
asics[0]['hashrate']=0.18
asics[0]['power']=360
asics[0]['price']=300
asics[0]['link']='https://en.bitcoin.it/wiki/Mining_hardware_comparison'

asics[1]['name']='Bitmain S2'
asics[1]['date']=date(year=2014,month=4,day=1)
asics[1]['hashrate']=1
asics[1]['power']=1100
asics[1]['price']=2260
asics[1]['link']='https://en.bitcoin.it/wiki/Mining_hardware_comparison'

asics[2]['name']='Bitmain S3'
asics[2]['date']=date(year=2014,month=7,day=1)
asics[2]['hashrate']=0.441
asics[2]['power']=340
asics[2]['price']=382
asics[2]['link']='https://en.bitcoin.it/wiki/Mining_hardware_comparison'

asics[3]['name']='Bitmain S4'
asics[3]['date']=date(year=2014,month=10,day=1)
asics[3]['hashrate']=2
asics[3]['power']=1400
asics[3]['price']=1400
asics[3]['link']='https://en.bitcoin.it/wiki/Mining_hardware_comparison'

asics[4]['name']='Bitmain S5'
asics[4]['date']=date(year=2015,month=1,day=1)
asics[4]['hashrate']=1.15
asics[4]['power']=590
asics[4]['price']=370
asics[4]['link']='https://en.bitcoin.it/wiki/Mining_hardware_comparison'

asics[5]['name']='Bitmain S7'
asics[5]['date']=date(year=2015,month=9,day=1)
asics[5]['hashrate']=4.86
asics[5]['power']=1210
asics[5]['price']=1823
asics[5]['link']='https://en.bitcoin.it/wiki/Mining_hardware_comparison'

asics[6]['name']='Bitmain S9'
asics[6]['date']=date(year=2016,month=8,day=1)
asics[6]['hashrate']=14
asics[6]['power']=1375
asics[6]['price']=2400
asics[6]['link']='https://en.bitcoin.it/wiki/Mining_hardware_comparison'

asics[7]['name']='Bitmain S9 shortage'
asics[7]['date']=date(year=2018,month=1,day=1)
asics[7]['hashrate']=14
asics[7]['power']=1375
asics[7]['price']=5179
asics[7]['link']='https://camelcamelcamel.com/Antminer-S9-~13TH-Bitcoin-12-1600/product/B01LX6EVNI'

asics[8]['name']='Pangolin whatsminer M10'
asics[8]['date']=date(year=2018,month=7,day=24)
asics[8]['hashrate']=33
asics[8]['power']=2150
asics[8]['price']=2000
asics[8]['link']='https://bitcointalk.org/index.php?topic=4737927.0'

asics[9]['name']='Pangolin whatsminer M20'
asics[9]['date']=date(year=2019,month=5,day=20)
asics[9]['hashrate']=48
asics[9]['power']=2300
asics[9]['price']=1450
asics[9]['link']='https://bitcointalk.org/index.php?topic=5120959.0'



dates=[]
jours=[]
price_per_tera=[]
electricity=[]
for i in range(0,10):
    machine=asics[i]
    dates.append(machine['date'])
    price_per_tera.append(machine['price']/machine['hashrate'])
    electricity.append(machine['power']/machine['hashrate'])
    jours.append((machine['date']-asics[0]['date']).days)

# linear regression to estimate the technical progress rate.
xbar=mean(jours)
num1=sum([yi*(xi-xbar) for yi,xi in zip(log(price_per_tera),jours)])
num2=sum([yi*(xi-xbar) for yi,xi in zip(log(electricity),jours)])
deno=sum([(xi-xbar)**2 for xi in jours])

print('a1: ',-365*num1/deno)
print('a2: ',-365*num2/deno)

lw=3 #linewidth
fg=(11.5,5)
ft='xx-large'

#***********************************************************************************************************
#                                       1st graph: the whole period with a in model halving
#***********************************************************************************************************

fig, ax = subplots(figsize=fg)
ax.plot(dates,log(electricity),linewidth=lw,color='red',label='Electricity consumption (log watt/Th/s)')
ax.plot(dates,log(electricity),'ro',linewidth=lw)
ax.plot(dates,log(price_per_tera),linewidth=lw,color='blue',label='Observed Price              (log $/Th/s)')
ax.plot(dates,log(price_per_tera),'bo',linewidth=lw)

# add the curve estimated with the model with variable costs. I0 = 1001 on 01/10/2014
I0 = 1002 # I0 estimated with the model with variable costs.
a = 0.85/365 # a estimated in the model with halvings.
xdates = [date_base(j) for j in range(1785, 3784)]
estimatedPrice = [log(I0)-a*(j-string_to_database("2014-10-01")) for j in range(1785,3784) ]
ax.plot(xdates, estimatedPrice, linewidth=lw, color='green', linestyle = ':', label = 'Calibrated price             (log $/Th/s)')

ax.tick_params(axis='both',labelsize=ft)
gcf().autofmt_xdate()
legend(fontsize=ft)
show()

#***********************************************************************************************************
#                                       1st graph: the whole period with a in baseline model
#***********************************************************************************************************

fig, ax = subplots(figsize=fg)
ax.plot(dates,log(electricity),linewidth=lw,color='red',label='Electricity consumption (log watt/Th/s)')
ax.plot(dates,log(electricity),'ro',linewidth=lw)
ax.plot(dates,log(price_per_tera),linewidth=lw,color='blue',label='Observed Price              (log $/Th/s)')
ax.plot(dates,log(price_per_tera),'bo',linewidth=lw)

# add the curve estimated with the model with variable costs. I0 = 1001 on 01/10/2014
I0 = 1002 # I0 estimated with the model with variable costs.
a = 0.76/365 # a estimated in the model with halvings.
xdates = [date_base(j) for j in range(1785, 3784)]
estimatedPrice = [log(I0)-a*(j-string_to_database("2014-10-01")) for j in range(1785,3784) ]
ax.plot(xdates, estimatedPrice, linewidth=lw, color='green', linestyle = ':', label = 'Calibrated price             (log $/Th/s)')

ax.tick_params(axis='both',labelsize=ft)
gcf().autofmt_xdate()
legend(fontsize=ft)
show()

#***********************************************************************************************************
#                   2nd graph: stop at last data point before end of 2nd period. a halving
#***********************************************************************************************************



fig, ax = subplots(figsize=fg)
ax.plot(dates[0:len(dates)-3],log(electricity[0:len(dates)-3]),linewidth=lw,color='red',label='Electricity consumption (log watt/Th/s)')
ax.plot(dates[0:len(dates)-3],log(electricity[0:len(dates)-3]),'ro',linewidth=lw)
ax.plot(dates[0:len(dates)-3],log(price_per_tera[0:len(dates)-3]),linewidth=lw,color='blue',label='Observed Price              (log $/Th/s)')
ax.plot(dates[0:len(dates)-3],log(price_per_tera[0:len(dates)-3]),'bo',linewidth=lw)

# add the curve estimated with the model with variable costs. I0 = 1001 on 01/10/2014
I0 = 1002 # I0 estimated with the model with variable costs.
a = 0.85/365 # a estimated in the model with halvings.
xdates = [date_base(j) for j in range(1785,2762)]
estimatedPrice = [log(I0)-a*(j-string_to_database("2014-10-01")) for j in range(1785,2762) ]

ax.plot(xdates, estimatedPrice, linewidth=lw, color='green', linestyle = ':', label = 'Calibrated price             (log $/Th/s)')

ax.tick_params(axis='both',labelsize=ft)
gcf().autofmt_xdate()
legend(fontsize='x-large')
show()

#***********************************************************************************************************
#       3rd graph: only 2nd period. (stop at last data point before end of 2nd period) a halving
#***********************************************************************************************************

fig, ax = subplots(figsize=fg)
ax.plot(dates[3:len(dates)-3],log(electricity[3:len(dates)-3]),linewidth=lw,color='red',label='Electricity consumption (log watt/Th/s)')
ax.plot(dates[3:len(dates)-3],log(electricity[3:len(dates)-3]),'ro',linewidth=lw)
ax.plot(dates[3:len(dates)-3],log(price_per_tera[3:len(dates)-3]),linewidth=lw,color='blue',label='Observed Price              (log $/Th/s)')
ax.plot(dates[3:len(dates)-3],log(price_per_tera[3:len(dates)-3]),'bo',linewidth=lw)

# add the curve estimated with the model with variable costs. I0 = 1001 on 01/10/2014
I0 = 1002 # I0 estimated with the model with variable costs.
a = 0.85/365 # a estimated in the model with halvings.
xdates = [date_base(j) for j in range(2091,2762)]
estimatedPrice = [log(I0)-a*(j-string_to_database("2014-10-01")) for j in range(2091,2762) ]
ax.plot(xdates, estimatedPrice, linewidth=lw, color='green', linestyle = ':', label = 'Calibrated price             (log $/Th/s)')

ax.tick_params(axis='both',labelsize=ft)
gcf().autofmt_xdate()
legend(fontsize='x-large')
show()
