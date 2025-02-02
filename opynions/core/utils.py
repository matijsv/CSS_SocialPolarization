''' Functions for accessing simulation results '''

import networkx as nx
import numpy as np
from opynions.core.simulation import run_sim


def get_graphs(n_runs, n_nodes, time_steps, epsilon, mu, m_generator=2):
    '''Simulates N_Runs networks and returns the final and initial graphs
    
    Args:
        n_runs: (int) number of runs
        n_nodes: (int) number of nodes
        time_steps: (int) number of time steps
        epsilon: (float bounds: [0,1]) threshold for opinion distance 
        mu: (float bounds: [0,1]) parameter for adjusting opinions
        m_generator: affects graph generation, see networkx.barabasi_albert_graph
    Returns:
        tuple containing:
            all_final_graphs: list of final graphs, length n_runs
            all_initial_graphs: list of initial graphs, length n_runs
    '''
    all_final_graphs = []
    all_initial_graphs = []
    for _ in range(n_runs):
        g_final, g_init = run_sim(n_nodes, time_steps, epsilon, mu, m_generator)
        all_final_graphs.append(g_final)
        all_initial_graphs.append(g_init)

    return all_final_graphs, all_initial_graphs

def get_opinion_hist(n_runs, n_nodes, time_steps, epsilon, mu, exclude_loners=False, m_generator=2):
    '''Simulates N_Runs networks and returns an array of arrays of opinions
    and the average distribution histogram
    
    Args:
        n_runs: (int) number of runs
        n_nodes: (int) number of nodes
        time_steps: (int) number of time steps
        epsilon: (float bounds: [0,1]) threshold for opinion distance 
        mu: (float bounds: [0,1]) parameter for adjusting opinions
    Returns:
        triple containing:
            all_opinions: array of arrays of opinions, shape (n_runs, n_nodes)
            average_histogram: average histogram of opinions, length 100
            avg_isolated: average number of isolated nodes
    
    Example usage:
        # If you want to plot the average histogram of opinions
        
        _, average_histogram = get_opinion_hist(1, 2000, 100, 0.1, 0.05)

        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 6))
        plt.bar(np.linspace(0, 1, len(average_histogram)),
            average_histogram, width=0.01, align='center')
        plt.xlabel('Opinion')
        plt.ylabel('Frequency')
        plt.show()
    '''
    all_histograms = []
    all_opinions = []
    all_isolated = []
    for _ in range(n_runs):
        # Run the simulation. Extract and store opinions
        g, _ = run_sim(n_nodes, time_steps, epsilon, mu, m_generator)
        all_isolated.append(len(list(nx.isolates(g))))
        if exclude_loners:
            g.remove_nodes_from(list(nx.isolates(g)))
        opinions = nx.get_node_attributes(g, 'opinion').values()
        all_opinions.append(opinions)
        # Create and store histogram for the current run
        hist, _ = np.histogram(list(opinions), bins=100, range=(0, 1))
        all_histograms.append(hist)

    avg_histogram = np.mean(all_histograms, axis=0) # Average the histograms
    avg_isolated = np.mean(all_isolated) # Average the number of isolated nodes
    return all_opinions, avg_histogram, avg_isolated

