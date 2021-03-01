""" plots the price and energy consumption of new machines against time
and compares with model calibration """

from datetime import date
from matplotlib.pyplot import subplots, gcf, legend, show
from numpy import log, exp
from data.get_data import load_data, as_datetime

def asics_data(black_and_white=False):
    
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

    asics[10]['name']='Antminer S19'
    asics[10]['date']=date(year=2020,month=8,day=1)
    asics[10]['hashrate']=110
    asics[10]['power']=3250
    asics[10]['price']=2493
    asics[10]['link']='https://bitcointalk.org/index.php?topic=5228802.msg54385576#msg54385576'


    dates=[]
    price_terahash_second=[]
    electricity=[]
    for i in range(0,11):
        machine=asics[i]
        dates.append(machine['date'])
        price_terahash_second.append(machine['price']/machine['hashrate'])
        electricity.append(machine['power']/machine['hashrate'])


    FIGURE_SIZE = (11.5, 5)
    FONT_SIZE = 'x-large'

    fig, ax = subplots(figsize=FIGURE_SIZE)
    if black_and_white:
        ax.plot(dates, log(electricity), linewidth=3, color='grey', label='Electricity consumption (log watt/Th/s)')
        ax.plot(dates, log(electricity), color='grey', marker= 'o', linewidth=3)
        ax.plot(dates, log(price_terahash_second), linewidth=3, color='silver', label='Observed Price              (log $/Th/s)')
        ax.plot(dates, log(price_terahash_second), color='silver', marker= 'o', linewidth=3)
    else:
        ax.plot(dates, log(electricity), linewidth=3, color='red', label='Electricity consumption (log watt/Th/s)')
        ax.plot(dates, log(electricity), 'ro', linewidth=3)
        ax.plot(dates, log(price_terahash_second), linewidth=3, color='blue', label='Observed Price              (log $/Th/s)')
        ax.plot(dates, log(price_terahash_second), 'bo',linewidth=3)

    technical_progress = 0.76/365  # estimated with baseline model, second period
    total_costs = 1825  # estimated with baseline model, second period
    number_days_interpoled_at_beginning = 306

    beginning_price_calibrated = asics[0]['price'] / asics[0]['hashrate']
    inferred_ratio_price_total_costs = beginning_price_calibrated * \
                                       exp(-number_days_interpoled_at_beginning * technical_progress) / total_costs
    print('inferred_ratio_price_total_costs: ', inferred_ratio_price_total_costs)
    print('total cost beginning: ', total_costs * exp(number_days_interpoled_at_beginning * technical_progress)) 

    days, R, Q, P, Q_initial = load_data('2013-11-28', '2020-08-09')

    estimatedPrice = [log(beginning_price_calibrated) - technical_progress * day for day in range(len(days)) ]
    if black_and_white:
        ax.plot(days, estimatedPrice, linewidth=3, color='k', linestyle = ':', label = 'Calibrated price             (log $/Th/s)')
    else:
        ax.plot(days, estimatedPrice, linewidth=3, color='green', linestyle = ':', label = 'Calibrated price             (log $/Th/s)')
    ax.tick_params(axis='both',labelsize=FONT_SIZE)

    ax.text(as_datetime('2013-11-01'), 6.9, 'S1', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2014-02-01'), 6.6, 'S2', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2014-05-01'), 6.2, 'S3', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2014-08-01'), 6.1, 'S4', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2014-12-01'), 5.3, 'S5', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2015-07-01'), 5, 'S7', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2016-03-01'), 4.2, 'Antminer S9', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2017-05-01'), 5.2, 'Antminer', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2017-09-01'), 4.7, 'S9', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2018-08-01'), 5.7, 'Pangolin', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2018-08-01'), 5.2, 'Whatsminer', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2018-08-01'), 4.7, 'M10', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2019-04-01'), 4.3, 'M20', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2020-03-01'), 4.5, 'Antminer', color='k', fontsize=FONT_SIZE)
    ax.text(as_datetime('2020-03-01'), 4, 'S19', color='k', fontsize=FONT_SIZE)

    
    gcf().autofmt_xdate()
    legend(fontsize=FONT_SIZE)
    show()

