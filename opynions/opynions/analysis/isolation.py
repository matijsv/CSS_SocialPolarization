'''Functions for analysis of disconnected nodes in the network. '''

import networkx as nx
from opynions.core.utils import get_graphs

def count_disconnected_nodes(graph):
    """
    Counts the number of disconnected nodes (isolates) in a given graph.

    Args:
        graph (networkx.Graph): The graph to analyze.
    Returns:
        int: Number of disconnected nodes (isolates).
    """
    return len(list(nx.isolates(graph)))

def analyze_disconnected_nodes(n_runs, n_nodes, time_steps, mu, epsilon_values):
    """
    Analyzes and counts the number of disconnected nodes for a range of epsilon values.

    Args:
        n_runs (int): Number of runs for each epsilon value.
        n_nodes (int): Number of nodes in the graph.
        time_steps (int): Number of time steps in the simulation.
        mu (float): Parameter for adjusting opinions.
        epsilon_values (list or numpy.ndarray): Range of epsilon values to test.

    Returns:
        list: Average number of disconnected nodes for each epsilon value.
    """
    avg_disconnected_nodes = []

    for epsilon in epsilon_values:
        print(f"Analyzing for epsilon = {epsilon:.3f}")
        total_disconnected = 0
       
        # Generate graphs for the given epsilon
        final_graphs, _ = get_graphs(n_runs, n_nodes, time_steps, epsilon, mu)

        # Count disconnected nodes in each graph and accumulate the total
        for graph in final_graphs:
            total_disconnected += count_disconnected_nodes(graph)

        # Compute the average number of disconnected nodes for this epsilon
        avg_disconnected = total_disconnected / n_runs
        avg_disconnected_nodes.append(avg_disconnected)

    return avg_disconnected_nodes