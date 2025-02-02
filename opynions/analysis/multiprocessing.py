''' Multiprocessing functions for generating dicts with data,
uses the combined analysis function in opynions.analysis.combined. '''

import multiprocessing as mp
import itertools
from opynions.analysis.combined import combined_analysis

def worker_all_both_params(epsilon, mu, n_runs, n_nodes, time_steps, m_generator):
    ''' Process manager, receives all parameters needed 
        and returns a dict full of the analysis results for that point
    '''
    results_dict = combined_analysis(n_runs, n_nodes, time_steps, epsilon, mu, m_generator)
    results_dict['epsilon'] = epsilon
    results_dict['mu'] = mu
    return results_dict

def multiprocess_all_both(epsilon_values, mu_values, n_runs, n_nodes, time_steps, m_generator):
    param_grid = list(itertools.product(epsilon_values, mu_values))
    num_workers = min(mp.cpu_count(), len(param_grid))
    with mp.Pool(num_workers) as pool:
        list_of_dicts = pool.starmap(worker_all_both_params, [(epsilon, mu, n_runs, n_nodes, time_steps, m_generator) for epsilon, mu in param_grid])

    return list_of_dicts