from models.basic_model import basic_model, basic_model_initial_parameters, plot_explanatory_graphs
from models.delay_model import delay_model, delay_model_initial_parameters
from models import finite_horizon_model 
from model_comparaison import models_hashrate_comparaison
from data.plot_data import plot_data, plot_exchange_rate
from data.asics_data import asics_data
from config import PERIOD_1_START, PERIOD_1_END, PERIOD_2_START, PERIOD_2_END,\
     PERIOD_3_START, PERIOD_3_END


# displays all numbers and graphs (coming from the Python code) in the article.

plot_explanatory_graphs()
plot_data()

for period in range(2, 3):
    basic_model.full_pipeline(eval(f'PERIOD_{period}_START'), eval(f'PERIOD_{period}_END'),\
                              basic_model_initial_parameters[f'{period}'], estimate_parameters=True)
    delay_model.full_pipeline(eval(f'PERIOD_{period}_START'), eval(f'PERIOD_{period}_END'),\
                              delay_model_initial_parameters[f'{period}'], estimate_parameters=True)
    # for the model with finite horizon, see the Matlab code.
    models_hashrate_comparaison(period)

asics_data()

finite_horizon_model.plot_comparaison_P(2)
plot_exchange_rate(PERIOD_2_START, PERIOD_2_END)


