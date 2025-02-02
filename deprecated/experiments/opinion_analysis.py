import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from opynions.core.utils import get_graphs

def compute_neighbor_similarity(graph):
    """
    Computes the average similarity of opinions between neighbors in the graph.

    Args:
        graph (networkx.Graph): The graph with 'opinion' as a node attribute.

    Returns:
        float: Average similarity of opinions between neighbors.
    """
    total_similarity = 0
    total_edges = 0

    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            opinion_node = graph.nodes[node]['opinion']
            opinion_neighbor = graph.nodes[neighbor]['opinion']
            total_similarity += 1 - abs(opinion_node - opinion_neighbor)  # Similarity is 1 - distance
            total_edges += 1

    if total_edges == 0:  # Avoid division by zero
        return 0

    return total_similarity / total_edges

def analyze_neighbor_similarity(N_runs, N_nodes, time_steps, mu, epsilon_values):
    """
    Analyzes and calculates the average neighbor similarity for a range of epsilon values.

    Args:
        N_runs (int): Number of runs for each epsilon value.
        N_nodes (int): Number of nodes in the graph.
        time_steps (int): Number of time steps in the simulation.
        mu (float): Parameter for adjusting opinions.
        epsilon_values (list or numpy.ndarray): Range of epsilon values to test.

    Returns:
        list: Average neighbor similarity values for each epsilon value.
    """
    avg_similarities = []

    for epsilon in epsilon_values:
        print(f"Analyzing neighbor similarity for epsilon = {epsilon:.3f}")
        total_similarity = 0

        # Generate graphs for the given epsilon
        final_graphs, _ = get_graphs(N_runs, N_nodes, time_steps, epsilon, mu)

        # Calculate neighbor similarity for each graph and accumulate the total
        for graph in final_graphs:
            total_similarity += compute_neighbor_similarity(graph)

        # Compute the average similarity for this epsilon
        avg_similarity = total_similarity / N_runs
        avg_similarities.append(avg_similarity)

    return avg_similarities

def plot_neighbor_similarity(epsilon_values, similarities):
    """
    Plots the neighbor similarity as a function of epsilon.

    Args:
        epsilon_values (list or numpy.ndarray): Epsilon values (x-axis).
        similarities (list): Neighbor similarity values (y-axis).
    """
    plt.figure(figsize=(10, 6))
    plt.plot(epsilon_values, similarities, marker='o', linestyle='-', color='b', label='Neighbor Similarity')
    plt.xlabel('Epsilon')
    plt.ylabel('Average Neighbor Similarity')
    plt.title('Neighbor Similarity vs Epsilon')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Parameters
    N_RUNS = 5           # Number of simulations per epsilon value
    N_NODES = 2000       # Number of nodes in each graph
    TIME_STEPS = 100     # Number of time steps
    MU = 0.25            # Adjustment parameter
    EPSILON_VALUES = np.linspace(0, 1, 20)  # Range of epsilon values (0 to 1 in 20 steps)

    # Analyze neighbor similarity for varying epsilon values
    similarities = analyze_neighbor_similarity(N_RUNS, N_NODES, TIME_STEPS, MU, EPSILON_VALUES)

    # Plot the results
    plot_neighbor_similarity(EPSILON_VALUES, similarities)
