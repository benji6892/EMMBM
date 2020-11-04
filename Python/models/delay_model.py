from util import compute_barrier, compute_P
from model import Model
from models.basic_model import total_costs as baseline_total_costs
from numpy import exp, inf, identity, array, arange
from math import floor, ceil

delay_model_initial_parameters = dict()
delay_model_initial_parameters['1'] = [0.003008, 21963, 11.5]
delay_model_initial_parameters['2'] = [0.002475, 5.1, 46.5]
delay_model_initial_parameters['3'] = [0.001824, 0.6, 43.5]


def simulationQdelay(parameters, R, Q_initial):

    a = parameters[0]
    B_tilde = parameters[1]
    delta = parameters[2]
    C0 = Q_initial
    T=len(R)
    Bt=B_tilde/exp(a*arange(1,T+1))
    C_sim=[]
    Q_sim=[]
    P_sim=[]
    C_sim.append(max(C0,R[0]/Bt[0]))
    Q_sim.append(C0)
    for t in range(1,T):
        C_sim.append(max(C_sim[-1],R[t]/Bt[t]))
    for t in range(0,abs(int(round(delta)))):
        Q_sim.append(C0)
    for t in range(abs(int(round(delta)))+1,T):    
        Q_sim.append((delta-floor(delta))*C_sim[t-int(ceil(delta))]\
                            +(ceil(delta)-delta)*C_sim[t-int(floor(delta))])
    return Q_sim


def objective_function(parameters, R, Q, P, Q_initial):
    if parameters[2] < 0.0001:
        return 1000000 + 1000000 * (0.0001 - parameters[2])
    else:
        Q_simulated = simulationQdelay(parameters, R, Q_initial)
        P_simulated = compute_P(R, Q_simulated)
        return sum([(p_sim - p)**2 for p_sim, p in zip(P_simulated, P)])


def total_costs(parameters, trend_brownian, var_brownian, interest_rate):
    delay = parameters[2]
    btc = baseline_total_costs(parameters, trend_brownian, var_brownian, interest_rate)
    return btc * exp((interest_rate - trend_brownian) * delay)

parameters_description = []
parameters_description.append({'name': 'rate of technical progress', 'multiply_by': 365})
parameters_description.append({'name': 'barrier_initial_value'})
parameters_description.append({'name': 'delay in days'})
delay_model = Model('model with time-to-build', parameters_description, simulationQdelay,\
                    total_costs, objective_function=objective_function)

