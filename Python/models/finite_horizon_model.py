import csv
from matplotlib.pyplot import subplots, gcf, legend, show
from matplotlib.dates import MonthLocator
from data.get_data import load_data, HALVINGS, as_datetime
from util import compute_P
from config import PERIOD_1_START, PERIOD_1_END, PERIOD_2_START, PERIOD_2_END,\
     PERIOD_3_START, PERIOD_3_END
from util import linestyles

def load_finite_horizon_model_data(period):
    Q_simulated = []
    barrier = []

    with open(f'data/finite_horizon_model_data/period{period}_data.csv') as csvfile:
        file = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in file:
            Q_simulated.append(float(row[0].replace(',', '.')))
            barrier.append(float(row[1].replace(',', '.')))

    return Q_simulated, barrier

# The model itself is implemented in Matlab

def plot_comparaison_P(period, black_and_white=False):

    days, R, Q, P, Q_initial = load_data(eval(f'PERIOD_{period}_START'),\
                                         eval(f'PERIOD_{period}_END'))
    Q_simulated, barrier = load_finite_horizon_model_data(period)
    P_simulated = compute_P(R, Q_simulated)

    FONT_SIZE = 'xx-large'
    fig, ax = subplots(figsize=(13, 5))
    if black_and_white:
        ax.plot(days, P, 'grey', linewidth=3, label='observed payoff')
        ax.plot(days, P_simulated, 'silver', linewidth=3, linestyle=linestyles['densely dashed'],
                label='simulated payoff')
        ax.plot(days, barrier, 'k', linewidth=3, linestyle='-.', label='barrier')
    else:
        ax.plot(days, P_simulated, 'b', linewidth=3, linestyle='--',
                label='simulated payoff')
        ax.plot(days, P, 'g', linewidth=3, label='observed payoff')
        ax.plot(days, barrier, 'r', linewidth=3, linestyle='-.', label='barrier')        
    for halving in HALVINGS:
        if halving in days:
            ax.axvline(x=halving, color='k', linestyle=':', linewidth=3, label='halving')
    ax.text(as_datetime('2015-04-01'), 4.5, 'Model with halvings', color='k', fontsize=FONT_SIZE)
    gcf().autofmt_xdate()
    ax.tick_params(axis='both', labelsize='xx-large')
    ax.xaxis.set_major_locator(MonthLocator(interval=6))
    ax.margins(0.03)
    legend(fontsize=FONT_SIZE)
    show()

    


    
    
