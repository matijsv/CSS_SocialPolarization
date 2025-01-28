'''All-in-one analysis function derived from the other analysis functions'''

import numpy as np
import networkx as nx
from networkx.algorithms.community import modularity
from networkx.algorithms.community import greedy_modularity_communities
from src.core.utils import get_graphs
from src.analysis.similarity import compute_neighbor_similarity

def combined_analysis(n_runs, n_nodes, time_steps, epsilon, mu):
    """
    Combines all analyses into one function, optimizes by reusing graph object,
    isolates lists and communities list.
    Included analyses: Variance, average isolates, average # communities, average modularity,
    and average similarity.

    Args:
        n_runs (int): The number of simulation runs to be averaged over.
        n_nodes (int): The number of nodes in the network.
        time_steps (int): The number of time steps to simulate.
        epsilon (float): Tolerance parameter (range: [0, 0.5]).
        mu (float): Convergence parameter (range: [0, 0.5]).
    
    Returns:
        
    """
    
    all_opinions = []
    all_isolated = 0
    all_num_communities = 0
    all_modularity = 0
    all_similarity = 0
    
    graphs, _ = get_graphs(n_runs, n_nodes, time_steps, epsilon, mu)
    
    for g in graphs:
        
        # aggregate opinions for variance
        all_opinions.append(nx.get_node_attributes(g, 'opinion').values())
        
        # count isolated nodes
        isolates_list = list(nx.isolates(g))
        all_isolated += len(isolates_list)
        
        # remove isolates from graph
        g.remove_nodes_from(isolates_list)
        # isolate and count communities
        communities = greedy_modularity_communities(g, resolution=0.001, best_n=7)
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
    

    return {"variance": variance, "avg_isolated": avg_isolated, 
            "avg_num_communities": avg_num_communities, "avg_modularity":avg_modularity,
            "avg_similarity": avg_similarity}