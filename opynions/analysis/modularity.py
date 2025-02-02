'''Functions for analyzing the number of communities and modularity of graphs.'''

import networkx as nx
from networkx.algorithms.community import modularity
from networkx.algorithms.community import greedy_modularity_communities
from opynions.core.utils import get_graphs
from opynions.settings import MODULARITY_RES
def count_communities(graph):
    """
    Counts the number of communities in a graph based on community detection.

    Args:
        graph (networkx.Graph): The graph for which to count communities.
    Returns:
        int: The number of communities in the graph.
    """
    # Use the greedy modularity communities detection algorithm
    # Remove isolates (nodes with no edges) from the graph
    graph.remove_nodes_from(list(nx.isolates(graph)))
    communities = greedy_modularity_communities(graph, resolution=MODULARITY_RES, best_n=7)
    # Count the number of communities
    num_communities = len(communities)
    return num_communities

def analyze_communities(n_runs, n_nodes, time_steps, mu, epsilon_values):
    """
    Analyzes and calculates the average number of communities 
    in graphs for a range of epsilon values.

    Args:
        n_runs (int): Number of runs for each epsilon value.
        n_nodes (int): Number of nodes in the graph.
        time_steps (int): Number of time steps in the simulation.
        mu (float): Parameter for adjusting opinions.
        epsilon_values (list): Range of epsilon values to test.

    Returns:
        list: Average number of communities for each epsilon value.
    """
    avg_communities = []

    for epsilon in epsilon_values:
        print(f"Analyzing communities for epsilon = {epsilon:.3f}")
        total_communities = 0

        # Generate graphs for the given epsilon
        final_graphs, _ = get_graphs(n_runs, n_nodes, time_steps, epsilon, mu)

        # Count communities for each graph and accumulate the total
        for graph in final_graphs:
            total_communities += count_communities(graph)

        # Compute the average number of communities for this epsilon
        avg_communities_value = total_communities / n_runs
        avg_communities.append(avg_communities_value)

    return avg_communities

def calculate_modularity(graph):
    """
    Calculates the modularity of a graph based on community detection.

    Args:
        graph (networkx.Graph): The graph for which to calculate modularity.
        exclude_isolates (boolean): Whether to exclude isolated nodes.
    Returns:
        float: The modularity of the graph.
    """
    # Use the greedy modularity communities detection algorithm
    # Remove isolates (nodes with no edges) from the graph
    graph.remove_nodes_from(list(nx.isolates(graph)))
    # Use the greedy modularity communities detection algorithm
    communities = greedy_modularity_communities(graph)
    # Calculate modularity
    mod_value = modularity(graph, communities)
    return mod_value

def analyze_modularity(n_runs, n_nodes, time_steps, mu, epsilon_values):
    """
    Analyzes and calculates the average modularity of graphs for a range of epsilon values.

    Args:
        n_runs (int): Number of runs for each epsilon value.
        n_nodes (int): Number of nodes in the graph.
        time_steps (int): Number of time steps in the simulation.
        mu (float): Parameter for adjusting opinions.
        epsilon_values (list or numpy.ndarray): Range of epsilon values to test.

    Returns:
        list: Average modularity values for each epsilon value.
    """
    avg_modularities = []

    for epsilon in epsilon_values:
        print(f"Analyzing modularity for epsilon = {epsilon:.3f}")
        total_modularity = 0

        # Generate graphs for the given epsilon
        final_graphs, _ = get_graphs(n_runs, n_nodes, time_steps, epsilon, mu)

        # Calculate modularity for each graph and accumulate the total
        for graph in final_graphs:
            total_modularity += calculate_modularity(graph)

        # Compute the average modularity for this epsilon
        avg_modularity = total_modularity / n_runs
        avg_modularities.append(avg_modularity)

    return avg_modularities