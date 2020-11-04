import sys
sys.path.append("..")
from matplotlib.pyplot import subplots, gcf, legend, show
from matplotlib.dates import DateFormatter, MonthLocator
from numpy import log, exp, arange
from util import compute_P
from data.get_data import load_data, load_exchange_rate, as_datetime

def plot_data():
    days, R, Q, P, Q_initial = load_data()

    FIG_SIZE = (10.8,5)
    FONT_SIZE = 'xx-large'
    fig, ax1 = subplots(figsize=FIG_SIZE)
    ax1.plot(days, log(R) ,'b',linewidth=3, label='log Rt', linestyle='--')
    ax1.set_ylabel('log Rt', color='b', fontsize=FONT_SIZE)
    ax1.tick_params(axis='y', colors='b', labelsize=FONT_SIZE)
    ax1.tick_params(axis='x', labelsize=FONT_SIZE)
    ax1.xaxis.set_major_formatter(DateFormatter('%Y'))
    gcf().autofmt_xdate()

    ax2 = ax1.twinx()
    ax2.plot(days, log(Q), 'r', linewidth=3, label='log Qt')
    ax2.set_ylabel('log Qt', color='r', fontsize=FONT_SIZE)
    ax2.tick_params(axis='y' ,colors='r', labelsize=FONT_SIZE)
    show()

    trend = 0.0014  # Moore law: 0.000959
    logP_detrended = [log(p) + trend * d for p,d in zip(P, range(len(P)))]

    fig, ax = subplots(figsize=FIG_SIZE)
    ax.plot(days, logP_detrended, linewidth=3,color='g',label=r'$log(P_t)+at$')
    ax.axvline(x=as_datetime('2013-04-01'),color='k',linestyle='dashed',linewidth=3)
    ax.axvline(x=as_datetime('2014-12-01'),color='k',linestyle='dashed',linewidth=3)
    ax.text(as_datetime('2011-10-01'),5,'GPUs',color='k',fontsize=FONT_SIZE)
    ax.text(as_datetime('2016-09-01'),5,'ASICs',color='k',fontsize=FONT_SIZE)
    ax.tick_params(axis='both',labelsize=FONT_SIZE)
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    legend(fontsize=FONT_SIZE)
    gcf().autofmt_xdate()
    show()


def plot_exchange_rate(date_from=None, date_to=None):

    days, exchange_rate = load_exchange_rate(date_from, date_to)

    FIG_SIZE = (13, 5)
    FONT_SIZE = 'xx-large'
    
    fig, ax = subplots(figsize=FIG_SIZE)
    ax.plot(days, exchange_rate, linewidth=3, label='exchange rate')
    ax.xaxis.set_major_locator(MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    gcf().autofmt_xdate()
    ax.tick_params(axis='both', labelsize=FONT_SIZE)
    legend(fontsize=FONT_SIZE)
    gcf().subplots_adjust(left=0.15)
    ax.margins(0.03)
    show()


