'''Functions for demonstrating the package.'''

import os
import numpy as np
from opynions.analysis.multiprocessing import multiprocess_all
from opynions.analysis.utils import list_of_dicts_to_csv, plot_subplots_from_csv

def slice_plots(epsilon, mu,
                n_runs, n_nodes, time_steps, m_ba, keep_csv=False):
    
    assert isinstance(epsilon, float) or isinstance(mu, float), "Either epsilon or mu must be a single float"
    
    if isinstance(epsilon, float):
        epsilon = [epsilon]
        varied_parameter = 'mu'
    if isinstance(mu, float):
        mu = [mu]
        varied_parameter = 'epsilon'
    
    assert all(0 <= val <= 1 for val in epsilon), "All epsilon values must be between 0 and 1"
    assert all(0 <= val <= 1 for val in mu), "All mu values must be between 0 and 1"
    
    
    list_of_dicts = multiprocess_all(epsilon_values=epsilon, mu_values=mu,
                                      n_runs=n_runs, n_nodes=n_nodes, time_steps=time_steps, m_ba=m_ba)

    list_of_dicts_to_csv(list_of_dicts, f'{varied_parameter}_slice.csv')

    plot_subplots_from_csv(f'{varied_parameter}_slice.csv', varied_parameter)
    
    if not keep_csv:
        os.remove(f'{varied_parameter}_slice.csv')
        
epsilon_values = np.linspace(0,0.5,51)
mu_value = 0.1

slice_plots(epsilon_values, mu_value, 20, 100, 10, 2)