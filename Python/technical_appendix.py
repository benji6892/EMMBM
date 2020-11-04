from matplotlib.pyplot import subplots, gcf, legend, show, ylim
from matplotlib.dates import DateFormatter, MonthLocator
from numpy import log, exp, diff, var, mean, array, arange, pi
from scipy.stats import gaussian_kde
from math import floor, sqrt
from data.get_data import load_data, load_number_blocks, as_datetime, load_q_data
from data.plot_data import plot_exchange_rate
from models.basic_model import basic_model, basic_model_initial_parameters
from models.reversible_model import reversible_model, reversible_model_initial_parameters
from models import finite_horizon_model 
from util import plot_comparaison_many_Q
from models.variable_costs_model import variable_costs_model,\
     variable_costs_model_initial_parameters
from config import PERIOD_1_START, PERIOD_1_END, PERIOD_2_START, PERIOD_2_END,\
     PERIOD_3_START, PERIOD_3_END


# displays all numbers and graphs (coming from the Python code) in the Technical Appendix, not yet in main.py

def plot_number_blocks_per_day():
    days, number_blocks = load_number_blocks()
    
    FIG_SIZE = (10.8, 3.5)
    FONT_SIZE = 'x-large'

    fig, ax = subplots(figsize=FIG_SIZE)
    ax.plot(days ,number_blocks , 'b', linewidth=3, label='daily number of blocks found')
    ax.plot(days, len(days) * [144 - 12 * 1.96], 'g', linewidth=3, label='95% bounds')
    ax.plot(days, len(days) * [144 + 12 * 1.96], 'g', linewidth=3)
    for day, linestyle, label in zip(['2011-04-01', '2013-01-31', '2014-10-01',\
                                      '2017-03-31', '2018-08-01', '2020-09-19'],\
                                     [':', ':', '--', '--', '-.', '-.'],\
                                     ['first period', None, 'second period', None, None, None]):
            ax.axvline(x=as_datetime(day), color='r', linestyle=linestyle,\
            linewidth=3, label=label)
    ax.tick_params(axis='both', labelsize=FONT_SIZE)
    ax.set_ylabel('daily number of blocks',fontsize=FONT_SIZE)
    ax.text(as_datetime('2011-05-09'), 350, '1st period', color='red', fontsize=FONT_SIZE)
    ax.text(as_datetime('2015-02-17'), 350,'2nd period', color='red', fontsize=FONT_SIZE)
    ax.text(as_datetime('2018-11-28'), 350,'3rd period', color='red', fontsize=FONT_SIZE)
    ax.text(as_datetime('2013-05-08'), 50, '95% confidence bounds', color='green', fontsize=FONT_SIZE)
    gcf().autofmt_xdate()
    ylim(0,400)
    ax.margins(0.03)
    show()


def plot_log_r_increments():

    def estimate_brownian_parameters_with_trimming(R, trim):
        N = sorted(diff(log(R)))
        M = N[int(floor(len(N)*trim/2)): int(floor(len(N)*(1-trim/2)))]
        sigma2 = var(M)
        mu = mean(N)   
        alpha = mu + 0.5 * sigma2
        return alpha, sigma2

    FONT_SIZE = 'xx-large'
    FIG_SIZE = (10.8, 2.7)

    days, R, Q, P, Q_initial = load_data()
    alpha, sigma2 = estimate_brownian_parameters_with_trimming(R, trim=0.1)

    M = diff([log(r) for r in R])
    density_M = gaussian_kde(M)

    gaussian_density = lambda x: exp(-(x+0.5*sigma2-alpha)**2/(2*sigma2))/sqrt(2*pi*sigma2)

    fig, ax = subplots(figsize=FIG_SIZE)
    support = [sqrt(sigma2) * p + alpha - 0.5 * sigma2 for p in arange(-5, 5, 0.01)]
    ax.plot(support, density_M.evaluate(support), 'r',\
         label='log R', linewidth=3, linestyle='--')
    ax.plot(support, gaussian_density(array(support)), 'b', linewidth=3,\
            label=r'$\mathcal{N}(\mu,\sigma ^2)$')
    ax.tick_params(axis='both', labelsize=FONT_SIZE)
    legend(fontsize=FONT_SIZE)
    ax.margins(0.03)
    show()


def out_of_sample_experiment():

    # estimate model parameters on period: 2014-10-01 -> 2015-04-15
    days, R, Q, P, Q_initial = load_data('2014-09-30', '2015-04-15')
    parameters = basic_model.estimate_parameters(R, Q, P, Q_initial, basic_model_initial_parameters['2'])
    
    # simulate and plot hashrate on whole period based on parameters estimated above
    days, R, Q, P, Q_initial = load_data('2014-09-30', '2017-03-31')
    Q_simulated = basic_model.Q_simulate(parameters, R, Q_initial)
    basic_model.plot_comparaison_Q(Q, Q_simulated, days)


def reversible_investment():
    days, R, Q, P, Q_initial = load_data('2011-03-31', '2013-01-31')

    reversible_hashrate = {'colour': 'b', 'linestyle': '--', 'label': 'log $Q^{sim}$ reversible'}
    baseline_hashrate = {'colour': 'g', 'linestyle': '-.', 'label': 'log $Q^{sim}$ baseline'}
    
    parameters_reversible = reversible_model.estimate_parameters(R, Q, P, Q_initial,\
                                                    reversible_model_initial_parameters['1'])
    reversible_hashrate['data'] = reversible_model.Q_simulate(parameters_reversible, R, Q_initial)
    baseline_hashrate['data'] = basic_model.Q_simulate(basic_model_initial_parameters['1'], R, Q_initial)

    plot_comparaison_many_Q(days, Q, (13, 5), reversible_hashrate, baseline_hashrate)


def construction_Q():
    days, Q_hat, probability_find_block, Q = load_q_data('2014-09-30', '2017-03-31')
    var=[q/(p*3600*24*10**12) for q,p in zip(Q, probability_find_block)] # first step estimator variance.
    bs=[q+1.96*sqrt(v) for q,v in zip(Q,var)]
    bi=[q-1.96*sqrt(v) for q,v in zip(Q,var)]

    FONT_SIZE='xx-large'
    
    lQ=log(Q)
    lQ_hat=log(Q_hat)
    lvar=[v/q**2 for v,q in zip(var,Q)] # variance computed with delta-method
    lbs=[lq+1.96*sqrt(lv) for lq,lv in zip(lQ,lvar)]
    lbi=[lq-1.96*sqrt(lv) for lq,lv in zip(lQ,lvar)]
    fig, ax = subplots(figsize=(11,5))
    ax.plot(days,lQ_hat,'b',linewidth=3,label=r'first step $log(\hat{Q})$')
    ax.plot(days,lQ,'r',linewidth=3,label=r'smoothed $log(\hat{Q})$',\
            linestyle='--')
    ax.plot(days,lbi,'g',linewidth=3,label='95% confidence bounds',\
            linestyle='-.')
    ax.plot(days,lbs,'g',linewidth=3,linestyle='-.')
    gcf().autofmt_xdate()
    ax.tick_params(axis='both',labelsize=FONT_SIZE)
    ax.margins(0.03)
    legend(fontsize=FONT_SIZE)
    show()
    
    

def model_with_variable_costs():
        variable_costs_model.full_pipeline(PERIOD_1_START , PERIOD_1_END,\
                                        variable_costs_model_initial_parameters['1'], estimate_parameters=True)
        variable_costs_model.full_pipeline(PERIOD_2_START , PERIOD_2_END,\
                                        variable_costs_model_initial_parameters['2'], estimate_parameters=True)

for period in [1, 3]:
    finite_horizon_model.plot_comparaison_P(period)
    plot_exchange_rate(eval(f'PERIOD_{period}_START'), eval(f'PERIOD_{period}_END'))

plot_number_blocks_per_day()

plot_log_r_increments()

out_of_sample_experiment()

reversible_investment()

construction_Q()

model_with_variable_costs()
