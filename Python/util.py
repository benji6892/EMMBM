from numpy import arange, exp, log
from data.get_data import HALVINGS
from matplotlib.pyplot import subplots, gcf, legend, show
from matplotlib.dates import MonthLocator
from collections import OrderedDict


def compute_barrier(initial_value, technical_progress, horizon):
    return initial_value / exp(technical_progress * arange(1, horizon + 1))


def compute_P(R, Q):
    return [r/q for r,q in zip(R, Q)]


def _plot_halvings_and_config(ax, days):
    for halving in HALVINGS:
        if halving in days:
            ax.axvline(x=halving, color='k', linestyle=':', linewidth=3, label='halving')
    gcf().autofmt_xdate()
    ax.tick_params(axis='both', labelsize='xx-large')
    ax.xaxis.set_major_locator(MonthLocator(interval=6))
    ax.margins(0.03)


def plot_comparaison_many_Q(days, Q, figure_size, *args, black_and_white=False):
    """
    each arg in arg must be a dictionnary with the following keys:
    data, colour, label, linestyle
    """
    fig, ax = subplots(figsize=figure_size)
    if black_and_white:
        ax.plot(days, log(Q), 'k', linewidth=3, label='log Q')
    else:
        ax.plot(days, log(Q), 'r', linewidth=3, label='log Q')
    for q in args:
        ax.plot(days, log(q['data']), q['colour'], linewidth=3,\
                linestyle=q['linestyle'], label=q['label'])
    _plot_halvings_and_config(ax, days)
    legend(fontsize = 'x-large')
    show()


linestyles = OrderedDict(
    [('solid',               (0, ())),
     ('loosely dotted',      (0, (1, 10))),
     ('dotted',              (0, (1, 5))),
     ('densely dotted',      (0, (1, 1))),

     ('loosely dashed',      (0, (5, 10))),
     ('dashed',              (0, (5, 5))),
     ('densely dashed',      (0, (5, 3))),

     ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('dashdotted',          (0, (3, 5, 1, 5))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),

     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])

