from models.basic_model import basic_model, basic_model_initial_parameters
from models.delay_model import delay_model, delay_model_initial_parameters
from models.variable_costs_model import variable_costs_model,\
     variable_costs_model_initial_parameters
from config import PERIOD_1_START, PERIOD_1_END, PERIOD_2_START, PERIOD_2_END,\
     PERIOD_3_START, PERIOD_3_END

BEGINNING_BLOCKS_PERIOD_1 = [0, 121, 277 ,417, 608]
BEGINNING_BLOCKS_PERIOD_2 = [0, 93, 272, 379, 479 ,606, 824]
BEGINNING_BLOCKS_PERIOD_3 = [0, 243, 449, 588, 712]

for period in range(1, 3):
    basic_model.block_bootstrap(eval(f'PERIOD_{period}_START'), eval(f'PERIOD_{period}_END'),\
                                eval(f'BEGINNING_BLOCKS_PERIOD_{period}'),\
                                basic_model_initial_parameters[f'{period}'])
    delay_model.block_bootstrap(eval(f'PERIOD_{period}_START'), eval(f'PERIOD_{period}_END'),\
                                eval(f'BEGINNING_BLOCKS_PERIOD_{period}'),\
                                delay_model_initial_parameters[f'{period}'])


for period in range(1, 3):
        variable_costs_model.block_bootstrap(eval(f'PERIOD_{period}_START'), eval(f'PERIOD_{period}_END'),\
                                             eval(f'BEGINNING_BLOCKS_PERIOD_{period}'),\
                                             variable_costs_model_initial_parameters[f'{period}'])
