from numpy import diff, log, inf, identity
from math import sqrt
from matplotlib.pyplot import subplots, gcf, legend, show, xticks, yticks

from model import Model
from data.get_data import load_data
from util import compute_barrier, compute_P

basic_model_initial_parameters = dict()
basic_model_initial_parameters['1'] = [0.0032334, 25996]
basic_model_initial_parameters['2'] = [0.00207, 5]
basic_model_initial_parameters['3'] = [0.00207, 0.6]

def simulationQ(parameters, R_sample, Q_initial):

    technical_progress = parameters[0]
    initial_barrier_value = parameters[1]
    horizon = len(R_sample)

    barrier = compute_barrier(initial_barrier_value, technical_progress, horizon) 
    Q_sim=[]
    Q_sim.append(max(Q_initial, R_sample[0] / initial_barrier_value))
    for t in range(1, horizon):
        Q_sim.append(max(Q_sim[-1], R_sample[t] / barrier[t]))
    return Q_sim


def total_costs(parameters, trend_brownian, var_brownian, interest_rate):

    def barrier_initial_expression(trend_brownian, var_brownian,
                               technical_progress_rate, interest_rate):
        A = (trend_brownian + technical_progress_rate - 0.5 * var_brownian)**2 +\
            2 * var_brownian * technical_progress_rate
        B = trend_brownian + technical_progress_rate
        return (0.5 * var_brownian - B + sqrt(A + 2 * var_brownian * interest_rate)) / var_brownian
    
    technical_progress_rate = parameters[0]
    barrier_initial_estimate = parameters[1]
    beta = barrier_initial_expression(trend_brownian, var_brownian,
                               technical_progress_rate, interest_rate)
    return barrier_initial_estimate * (beta - 1) / (beta * (interest_rate - trend_brownian))


def plot_explanatory_graphs(black_and_white=False):
    days, R, Q, P, Q_initial = load_data('2014-09-30', '2017-03-31')
    Q_sim = simulationQ((0.00207, 5.3), R, Q_initial)
    P_sim = compute_P(R, Q_sim)
    barrier = compute_barrier(5.3, 0.00207, len(R))

    FONT_SIZE = 'xx-large'
    FIGURE_SIZE = (10.8, 2.7)
    fig, ax = subplots(figsize=FIGURE_SIZE)
    if black_and_white:
        ax.plot(days, barrier, 'k', linewidth=3, label='barrier', linestyle='dashed')
        ax.plot(days, P_sim, 'grey', linewidth=3, label='payoff')
    else:
        ax.plot(days, barrier, 'r', linewidth=3, label='barrier', linestyle='dashed')
        ax.plot(days, P_sim, 'g', linewidth=3, label='payoff')
    gcf().autofmt_xdate()
    legend(fontsize=FONT_SIZE)
    ax.set_xlabel('time',fontsize=FONT_SIZE)
    xticks([])
    yticks([])
    ax.margins(0.03)
    show()

    fig, ax = subplots(figsize=FIGURE_SIZE)
    if black_and_white:
        ax.plot(days, log(Q_sim), 'k', linewidth=3, label='computing power')
    else:
        ax.plot(days, log(Q_sim), 'b', linewidth=3, label='computing power')
    gcf().autofmt_xdate()
    legend(fontsize=FONT_SIZE)
    ax.set_xlabel('time',fontsize=FONT_SIZE)
    xticks([])
    yticks([])
    ax.margins(0.03)
    show()
    
parameters_description = []
parameters_description.append({'name': 'rate of technical progress', 'multiply_by': 365})
parameters_description.append({'name': 'barrier_initial_value'})
basic_model = Model('basic model', parameters_description, simulationQ, total_costs)


