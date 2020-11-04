from numpy import exp
from model import Model

reversible_model_initial_parameters = dict()
reversible_model_initial_parameters['1'] = [0.003, 2767]

def simulation_Q(parameters, R, Q_initial):
    a = parameters[0]
    C0 = parameters[1]
    return [(r/C0) * exp(-a*t) for (r,t) in zip(R, range(len(R)))]

parameters_description = []
parameters_description.append({'name': 'rate of technical progress', 'multiply_by': 365})
parameters_description.append({'name': 'initial electricity cost per Th/s'})
reversible_model = Model('model with reversible investments', parameters_description,\
                         simulation_Q, None)

