'''Functions for demonstrating the package.'''

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from opynions.analysis.multiprocessing import multiprocess_all
from opynions.analysis.utils import list_of_dicts_to_csv, plot_subplots_from_csv, create_heatmap_from_csv

def slice_plots(epsilon, mu, n_runs, n_nodes, time_steps, m_ba, keep_csv=False):
    """
    Generates and saves slice plots by varying either epsilon or mu parameter.
    
    Parameters:
    
        epsilon (float or list of floats): Epsilon value(s) to be used in the simulation.
        mu (float or list of floats): Mu value(s) to be used in the simulation.
        n_runs (int): Number of runs for the simulation.
        n_nodes (int): Number of nodes in the network.
        time_steps (int): Number of time steps for the simulation.
        m_ba (int): Parameter for the Barabási–Albert model. See networkx.barabasi_albert_graph()
        keep_csv (bool, optional): If True, the generated CSV file will be kept. Defaults to False.
    
    Raises:
        AssertionError: If neither epsilon nor mu is a single float.
        AssertionError: If both epsilon and mu are single floats.
        AssertionError: If neither epsilon nor mu is a list or numpy array.
        AssertionError: If any value in epsilon is not between 0 and 1.
        AssertionError: If any value in mu is not between 0 and 1.
    
    Returns:
        None
    """

    assert isinstance(epsilon, float) or isinstance(mu, float), "Either epsilon or mu must be a single float"
    assert not (isinstance(epsilon, float) and isinstance(mu, float)), "Both epsilon and mu cannot be single floats, one must be an array"
    assert isinstance(epsilon, (list, np.ndarray)) or isinstance(mu, (list, np.ndarray)), "At least one of epsilon or mu must be a list or numpy array"
    
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
    plt.show()
    pass

def create_heatmaps(epsilon, mu, n_runs, n_nodes, time_steps, m_ba, file_path = 'heatmap.csv', keep_csv=True):
    """
    Generates heatmaps based on the provided parameters and saves the data for them to a CSV file.
    If the CSV file already exists, it wont regenerate the data (wasting time), and just plot the heatmaps.
    
    Parameters:
        epsilon (list): A list of epsilon values, each between 0 and 1.
        mu (list): A list of mu values, each between 0 and 1.
        n_runs (int): The number of runs to perform.
        n_nodes (int): The number of nodes in the network.
        time_steps (int): The number of time steps for the simulation.
        m_ba (int): The parameter for the Barabási–Albert model.
        file_path (str, optional): The path to the CSV file where the heatmap data will be saved. Defaults to 'heatmap.csv'.
        keep_csv (bool, optional): Whether to keep the CSV file after creating the heatmap. Defaults to True.
    Raises:
        AssertionError: If epsilon or mu are not lists, or if their values are not between 0 and 1.
    Returns:
        None
    """
    
    assert isinstance(epsilon, (list, np.ndarray)) and isinstance(mu, (list, np.ndarray)), "Both epsilon and mu must be lists or numpy arrays"
    assert all(0 <= val <= 1 for val in epsilon), "All epsilon values must be between 0 and 1"
    assert all(0 <= val <= 1 for val in mu), "All mu values must be between 0 and 1"
    
    if not os.path.exists(file_path):
        list_of_dicts = multiprocess_all(epsilon_values=epsilon, mu_values=mu,
                                          n_runs=n_runs, n_nodes=n_nodes, time_steps=time_steps, m_ba=m_ba)
        list_of_dicts_to_csv(list_of_dicts, file_path)
 
    df = pd.read_csv(file_path)
    for column in df.columns:
        if column not in ['mu', 'epsilon']:
            create_heatmap_from_csv(file_path, column, 'mu', 'epsilon')
            
    if not keep_csv:
        os.remove(file_path)
        
    plt.show()
    pass