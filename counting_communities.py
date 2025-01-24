from networkx.algorithms.community import greedy_modularity_communities 
from utils import get_graphs
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

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
    communities = greedy_modularity_communities(graph, resolution=0.1, best_n=7)
    # Count the number of communities
    num_communities = len(communities)
    return num_communities

def analyze_communities(N_runs, N_nodes, time_steps, mu, epsilon_values):
    """
    Analyzes and calculates the average number of communities in graphs for a range of epsilon values.

    Args:
        N_runs (int): Number of runs for each epsilon value.
        N_nodes (int): Number of nodes in the graph.
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
        final_graphs, _ = get_graphs(N_runs, N_nodes, time_steps, epsilon, mu)

        # Count communities for each graph and accumulate the total
        for graph in final_graphs:
            total_communities += count_communities(graph)
        
        # Compute the average number of communities for this epsilon
        avg_communities_value = total_communities / N_runs
        avg_communities.append(avg_communities_value)   
    
    return avg_communities

def plot_communities(epsilon_values, communities):
    """
    Plots the number of communities as a function of epsilon.

    Args:
        epsilon_values (list or numpy.ndarray): Range of epsilon values.
        communities (list): Average number of communities for each epsilon value.
    """
    plt.figure()
    plt.plot(epsilon_values, communities, marker='o', color='b')
    plt.title("Number of Communities vs. Epsilon")
    plt.xlabel("Epsilon")
    plt.ylabel("Number of Communities")
    plt.grid(True)
    plt.show()
    
# Set the parameters
N_runs = 5
N_nodes = 2000
time_steps = 100
mu = 0.25
epsilon_values =  np.linspace(0.0, 0.5, num=5)
num_communities = analyze_communities(N_runs, N_nodes, time_steps, mu, epsilon_values)

plot_communities(epsilon_values, num_communities)