from simulation import run_sim
import networkx as nx
import numpy as np

# DEFAULT PARAMETERS
# N_RUNS = 5
# N_NODES = 2000
# TIME_STEPS = 100
# MU = 0.25

def get_graphs(N_runs, N_nodes, time_steps, epsilon, mu):
    '''Simulates N_Runs networks and returns the final and initial graphs
    
    Args:
        N_runs: (int) number of runs
        N_nodes: (int) number of nodes
        time_steps: (int) number of time steps
        epsilon: (float bounds: [0,1]) threshold for opinion distance 
        mu: (float bounds: [0,1]) parameter for adjusting opinions
    Returns:
        tuple containing:
            all_final_graphs: list of final graphs, length N_runs
            all_initial_graphs: list of initial graphs, length N_runs
    '''
    all_final_graphs = []
    all_initial_graphs = []
    for _ in range(N_runs):
        g_final, g_init = run_sim(N_nodes, T=time_steps, epsilon=epsilon, mu=mu, plot=False, progress_bar=False)
        all_final_graphs.append(g_final)
        all_initial_graphs.append(g_init)
        
    return all_final_graphs, all_initial_graphs

def get_opinion_hist(N_runs, N_nodes, time_steps, epsilon, mu):
    '''Simulates N_Runs networks and returns an array of arrays of opinions and the average histogram
    
    Args:
        N_runs: (int) number of runs
        N_nodes: (int) number of nodes
        time_steps: (int) number of time steps
        epsilon: (float bounds: [0,1]) threshold for opinion distance 
        mu: (float bounds: [0,1]) parameter for adjusting opinions
    Returns:
        tuple containing:
            all_opinions: array of arrays of opinions, shape (N_runs, N_nodes)
            average_histogram: average histogram of opinions, length 100
    
    Example usage:
        # If you want to plot the average histogram of opinions
        
        _, average_histogram = get_opinion_hist(1, 2000, 100, 0.1, 0.05)

        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 6))
        plt.bar(np.linspace(0, 1, len(average_histogram)), average_histogram, width=0.01, align='center')
        plt.xlabel('Opinion')
        plt.ylabel('Frequency')
        plt.show()
    '''
    all_histograms = []
    all_opinions = []
    
    for _ in range(N_runs):
        # Run the simulation. Extract and store opinions
        g, _ = run_sim(N_nodes, T=time_steps, epsilon=epsilon, mu=mu, plot=False, progress_bar=False)
        opinions = nx.get_node_attributes(g, 'opinion').values()
        all_opinions.append(opinions)
        # Create and store histogram for the current run
        hist, _ = np.histogram(list(opinions), bins=100, range=(0, 1))
        all_histograms.append(hist)
        
    avg_histogram = np.mean(all_histograms, axis=0) # Average the histograms
    
    return all_opinions, avg_histogram
