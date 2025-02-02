'''All-in-one analysis function derived from the other analysis functions'''

import numpy as np
import networkx as nx
from networkx.algorithms.community import modularity
from networkx.algorithms.community import greedy_modularity_communities
from opynions.core.utils import get_graphs
from opynions.analysis.similarity import compute_neighbor_similarity
from opynions.settings import MODULARITY_RES

def combined_analysis(n_runs, n_nodes, time_steps, epsilon, mu, m_ba=2):
    """
    Combines all analyses into one function, optimizes by reusing graph object,
    isolates lists and communities list. NOTE: for a single combination of epsilon and mu.
    Included analyses: Variance, average isolates, average # communities, average modularity,
    and average similarity.

    Args:
        n_runs (int): The number of simulation runs to be averaged over.
        n_nodes (int): The number of nodes in the network.
        time_steps (int): The number of time steps to simulate.
        epsilon (float): Tolerance parameter (range: [0, 0.5]).
        mu (float): Convergence parameter (range: [0, 0.5]).
        m_generato (int): affects graph generation, see networkx.barabasi_albert_graph()
    
    Returns:
        dict: containing all analyses with keys:
            - "variance": Variance of opinions across all runs.
            - "num_isolates": Average number of isolated nodes across all runs.
            - "num_communities": Average number of communities across all runs.
            - "modularity": Average modularity score across all runs.
            - "similarity": Average neighbor similarity across all runs.
    """
    
    all_opinions = []
    all_isolated = 0
    all_num_communities = 0
    all_modularity = 0
    all_similarity = 0
    
    graphs, _ = get_graphs(n_runs, n_nodes, time_steps, epsilon, mu, m_ba)
    
    for g in graphs:
        
        # aggregate opinions for variance
        all_opinions.append(nx.get_node_attributes(g, 'opinion').values())
        
        # count isolated nodes
        isolates_list = list(nx.isolates(g))
        all_isolated += len(isolates_list)
        
        # remove isolates from graph
        g.remove_nodes_from(isolates_list)
        # isolate and count communities
        communities = greedy_modularity_communities(g, resolution=MODULARITY_RES, best_n=7)
        all_num_communities += len(communities)
        # use same list for modularity value
        all_modularity += modularity(g, communities)
        
        # similarity
        all_similarity += compute_neighbor_similarity(g)
        
    #calculate variance from all opinions
    flattened_opinions = [opinion for run in all_opinions for opinion in run]
    variance = np.var(flattened_opinions)
    
    # average aggregates
    num_runs = len(graphs) 
    avg_isolated = all_isolated / num_runs 
    avg_num_communities = all_num_communities / num_runs
    avg_modularity = all_modularity / num_runs
    avg_similarity = all_similarity / num_runs
    

    return {"variance": variance, "num_isolates": avg_isolated, 
            "num_communities": avg_num_communities, "modularity":avg_modularity,
            "similarity": avg_similarity}
    
def modules_communities_analysis(n_runs, n_nodes, time_steps, epsilon, mu):
    """
    Included analyses: average # communities, average modularity,

    Args:
        n_runs (int): The number of simulation runs to be averaged over.
        n_nodes (int): The number of nodes in the network.
        time_steps (int): The number of time steps to simulate.
        epsilon (float): Tolerance parameter (range: [0, 0.5]).
        mu (float): Convergence parameter (range: [0, 0.5]).
    
    Returns:
        dict: containing all analyses with keys:
            - "avg_num_communities": Average neighbor similarity across all runs.
            - "avg_modularity": Average modularity score across all runs.
    """
    
    all_num_communities = 0
    all_modularity = 0
    
    graphs, _ = get_graphs(n_runs, n_nodes, time_steps, epsilon, mu)
    
    for g in graphs:
        
        # remove isolates from graph
        isolates_list = list(nx.isolates(g))
        g.remove_nodes_from(isolates_list)
        # isolate and count communities
        communities = greedy_modularity_communities(g, resolution=0.1, best_n=7)
        all_num_communities += len(communities)
        # use same list for modularity value
        all_modularity += modularity(g, communities)
    
    # average aggregates
    num_runs = len(graphs) 
    avg_num_communities = all_num_communities / num_runs
    avg_modularity = all_modularity / num_runs
    

    return {"avg_num_communities": avg_num_communities, "avg_modularity":avg_modularity}