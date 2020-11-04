from numpy import arange, exp, log
from data.get_data import HALVINGS
from matplotlib.pyplot import subplots, gcf, legend, show
from matplotlib.dates import MonthLocator


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


def plot_comparaison_many_Q(days, Q, figure_size, *args):
    """
    each arg in arg must be a dictionnary with the following keys:
    data, colour, label, linestyle
    """
    fig, ax = subplots(figsize=figure_size)
    ax.plot(days, log(Q), 'r', linewidth=3, label='log Q')
    for q in args:
        ax.plot(days, log(q['data']), q['colour'], linewidth=3,\
                linestyle=q['linestyle'], label=q['label'])
    _plot_halvings_and_config(ax, days)
    legend(fontsize = 'xx-large')
    show()

    

