from scipy.optimize import minimize
from numpy import array, log, exp, diff, var, mean, std
from matplotlib.pyplot import subplots, gcf, legend, show
from matplotlib.dates import MonthLocator
from util import compute_barrier, compute_P
from random import seed, randint
from math import floor
from data.get_data import load_data, HALVINGS, as_datetime
from util import linestyles

FIGURE_SIZE = (13, 5)
LINEWIDTH = 3
FONT_SIZE = 'xx-large'


def estimate_brownian_parameters(R):
    M = diff(log(R))
    sigma2 = var(M)
    alpha = mean(M) + 0.5 * sigma2
    return alpha, sigma2
    

class Model:

    def __init__(self, model_name, parameters_description, simulation_function,\
                 total_costs, objective_function=None):
        self.model_name = model_name
        self.parameters_description = parameters_description
        self.Q_simulate = simulation_function
        self.total_costs = total_costs
        self.objective_function = objective_function if objective_function is not None else self.default_objective_function
        self.interest_rate = 0.1 / 365

    def full_pipeline(self, date_from, date_to, parameters, estimate_parameters = False):
        days, R, Q, P, Q_initial = load_data(date_from, date_to)
        print('\n\nModel: ', self.model_name, '   ',days[0].strftime('%Y-%m-%d'), ' -> ',\
              days[-1].strftime('%Y-%m-%d'),'\n')
        if estimate_parameters:
            parameters = self.estimate_parameters(R, Q, P, Q_initial, parameters)
        Q_simulated = self.Q_simulate(parameters, R, Q_initial)
        self.display_parameters(parameters)
        P_simulated = compute_P(R, Q_simulated)
        barrier = compute_barrier(parameters[1], parameters[0], len(R))
        trend_brownian, var_brownian = estimate_brownian_parameters(R)
        print('trend_brownian: ', 365 * trend_brownian)
        print('var brownian: ', 365 * var_brownian)
        print('total costs: ',self.total_costs(parameters, trend_brownian, var_brownian, self.interest_rate))
        self.plot_comparaison_Q(Q, Q_simulated, days)
        self.plot_comparaison_P(P, P_simulated, barrier, days)

    def default_objective_function(self, parameters, R, Q, P, Q_initial):       
        Q_simulated = self.Q_simulate(parameters, R, Q_initial)
        return sum([(q_sim - q)**2 / q**2 for q_sim, q in zip(Q_simulated, Q)])

    def estimate_parameters(self, R, Q, P, Q_initial, parameters_initial_values):
        return minimize(self.objective_function, array(parameters_initial_values),\
                        args=(R, Q, P, Q_initial),\
                        method='Nelder-Mead', options={'xtol': 1e-8, 'disp': False})['x']

    @staticmethod
    def _plot_halvings_and_config(ax, days):
        for halving in HALVINGS:
            if halving in days:
                ax.axvline(x=halving, color='k', linestyle=':', linewidth=LINEWIDTH, label='halving')
        gcf().autofmt_xdate()
        ax.tick_params(axis='both', labelsize=FONT_SIZE)
        ax.xaxis.set_major_locator(MonthLocator(interval=6))
        ax.margins(0.03)

    def plot_comparaison_Q(self, Q, Q_simulated, days, black_and_white=False):
        fig, ax = subplots(figsize=FIGURE_SIZE)
        if black_and_white:
            ax.plot(days, log(Q), 'k', linewidth=LINEWIDTH, label='log Q')
            ax.plot(days, log(Q_simulated), 'k', linestyle='--',
                    linewidth=LINEWIDTH, label=r'log $Q^{sim}$')
        else:
            ax.plot(days, log(Q), 'r', linewidth=LINEWIDTH, label='log Q')
            ax.plot(days, log(Q_simulated), 'b', linestyle='--',
                    linewidth=LINEWIDTH, label=r'log $Q^{sim}$')
        self._plot_halvings_and_config(ax, days)
        legend(fontsize = FONT_SIZE)
        show()

    def plot_comparaison_P(self, P, P_simulated, barrier, days, black_and_white=False):
        fig, ax = subplots(figsize=FIGURE_SIZE)
        if black_and_white:
            ax.plot(days, P, 'grey', linewidth=LINEWIDTH, label='observed payoff')
            ax.plot(days, P_simulated, 'silver', linewidth=LINEWIDTH, linestyle=linestyles['densely dashed'],
                    label='simulated payoff')
            ax.plot(days, barrier, 'k', linewidth=LINEWIDTH, linestyle='-.', label='barrier')
        else:
            ax.plot(days, P_simulated, 'b', linewidth=LINEWIDTH, linestyle='--',
                    label='simulated payoff')
            ax.plot(days, P, 'g', linewidth=LINEWIDTH, label='observed payoff')
            ax.plot(days, barrier, 'r', linewidth=LINEWIDTH, linestyle='-.', label='barrier')
        legend(fontsize = FONT_SIZE)
        self._plot_halvings_and_config(ax, days)
        show()

    def display_parameters(self, parameters):
        for i in range(len(parameters)):
            if 'multiply_by' in self.parameters_description[i]:
                multiply_by = self.parameters_description[i]['multiply_by']
            else:
                multiply_by = 1
            print(self.parameters_description[i]['name'],': ', parameters[i] * multiply_by)
        

    @staticmethod
    def _create_bootstrap_sample(blocks_begin, R_returns, Q_returns, R_initial, Q_initial):
        blocks_end = [begin for begin in blocks_begin[1:]] + [len(R_returns) + 1] 
        number_blocks = len(blocks_begin)
        blocks_sample = [randint(0, number_blocks - 1) for i in range(0, number_blocks)]
        R_returns_bootstrap = [] 
        Q_returns_bootstrap = [] 
        for block_index in blocks_sample:
            R_returns_bootstrap += list(R_returns[blocks_begin[block_index] : blocks_end[block_index]])
            Q_returns_bootstrap += list(Q_returns[blocks_begin[block_index] : blocks_end[block_index]])
        R_sample_bootstrap = [R_initial] 
        Q_sample_bootstrap = [Q_initial] 
        for r in R_returns_bootstrap:
            R_sample_bootstrap.append(R_sample_bootstrap[-1] * r)
        for q in Q_returns_bootstrap:
            Q_sample_bootstrap.append(Q_sample_bootstrap[-1] * q)
        return R_sample_bootstrap, Q_sample_bootstrap

    def block_bootstrap(self, date_from, date_to, blocks_begin, parameters, number_draws=1000):
        seed(1)
        days, R, Q, P, Q_initial = load_data(date_from, date_to)
        R_returns = exp(diff(log(R))) 
        Q_returns = exp(diff(log(Q)))
        estimates = list()
        costs = list()
        print('\n\nBootstrap ', self.model_name, '   ',days[0].strftime('%Y-%m-%d'), ' -> ',\
              days[-1].strftime('%Y-%m-%d'),'\n')
        for draw in range(0, number_draws):
            print(draw + 1, '/', number_draws)
            R_sample_bootstrap, Q_sample_bootstrap = self._create_bootstrap_sample(\
                blocks_begin, R_returns, Q_returns, R[0], Q[0])
            P_sample_bootstrap = compute_P(R_sample_bootstrap, Q_sample_bootstrap)
            estimated_parameters_bootstrap = self.estimate_parameters(\
                R_sample_bootstrap, Q_sample_bootstrap, P, Q_initial, parameters)
            # rate of technical progress cannot be negative.
            estimated_parameters_bootstrap[0] = max(estimated_parameters_bootstrap[0], 0)
            trend_brownian_bootstrap, var_brownian_bootstrap = estimate_brownian_parameters(R_sample_bootstrap)
            costs.append(self.total_costs(estimated_parameters_bootstrap, trend_brownian_bootstrap,\
                                          var_brownian_bootstrap, self.interest_rate))
            estimates.append(estimated_parameters_bootstrap)

        print('\nparameters standard deviation:')
        self.display_parameters([std([estimate[i] for estimate in estimates]) for i in range(0, len(parameters))])
        print('total costs standard deviation :',std(costs))


        
        
        
        

    

