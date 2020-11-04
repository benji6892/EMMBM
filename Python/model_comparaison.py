from data.get_data import load_data
from config import PERIOD_1_START, PERIOD_1_END, PERIOD_2_START, PERIOD_2_END, PERIOD_3_START, PERIOD_3_END
from models.basic_model import basic_model, basic_model_initial_parameters
from models.delay_model import delay_model, delay_model_initial_parameters
from models.finite_horizon_model import load_finite_horizon_model_data
from util import plot_comparaison_many_Q


def models_hashrate_comparaison(period):
    
    days, R, Q, P, Q_initial = load_data(eval(f'PERIOD_{str(period)}_START'), eval(f'PERIOD_{str(period)}_END'))
    Q_sim_halving, barrier_halving = load_finite_horizon_model_data(period)

    delay_hashrate = {'colour': 'm', 'linestyle': '-.', 'label': r'log $Q^{sim}$ delay'}
    baseline_hashrate = {'colour': 'g', 'linestyle': ':', 'label': 'log $Q^{sim}$ baseline'}
    finite_horizon_hashrate = {'colour': 'b', 'linestyle': '--', 'label': r'log $Q^{sim}$ halving'}

    baseline_hashrate['data'] = basic_model.Q_simulate(basic_model_initial_parameters[str(period)], R, Q_initial)
    delay_hashrate['data'] = delay_model.Q_simulate(delay_model_initial_parameters[str(period)], R, Q_initial)
    finite_horizon_hashrate['data'] = Q_sim_halving

    plot_comparaison_many_Q(days, Q, (13, 5), baseline_hashrate, delay_hashrate, finite_horizon_hashrate)

