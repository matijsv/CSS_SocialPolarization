import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from utils import get_graphs

def count_disconnected_nodes(graph):
    """
    Counts the number of disconnected nodes (isolates) in a given graph.

    Args:
        graph (networkx.Graph): The graph to analyze.
    Returns:
        int: Number of disconnected nodes (isolates).
    """
    return len(list(nx.isolates(graph)))

def analyze_disconnected_nodes(N_runs, N_nodes, time_steps, mu, epsilon_values):
    """
    Analyzes and counts the number of disconnected nodes for a range of epsilon values.

    Args:
        N_runs (int): Number of runs for each epsilon value.
        N_nodes (int): Number of nodes in the graph.
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
        final_graphs, _ = get_graphs(N_runs, N_nodes, time_steps, epsilon, mu)

        # Count disconnected nodes in each graph and accumulate the total
        for graph in final_graphs:
            total_disconnected += count_disconnected_nodes(graph)
        
        # Compute the average number of disconnected nodes for this epsilon
        avg_disconnected = total_disconnected / N_runs
        avg_disconnected_nodes.append(avg_disconnected)
    
    return avg_disconnected_nodes

def plot_disconnected_nodes(epsilon_values, disconnected_nodes):
    """
    Plots the number of disconnected nodes as a function of epsilon.

    Args:
        epsilon_values (list or numpy.ndarray): Epsilon values (x-axis).
        disconnected_nodes (list): Number of disconnected nodes (y-axis).
    """
    plt.figure(figsize=(10, 6))
    plt.plot(epsilon_values, disconnected_nodes, marker='o', linestyle='-', color='b', label='Disconnected Nodes')
    plt.xlabel('Epsilon')
    plt.ylabel('Number of Disconnected Nodes')
    plt.title('Disconnected Nodes vs Epsilon')
    plt.grid(True)
    plt.legend()
    plt.show()

# use
if __name__ == "__main__":
    # Parameters
    N_RUNS = 5           # Number of simulations per epsilon value
    N_NODES = 2000       # Number of nodes in each graph
    TIME_STEPS = 100     # Number of time steps
    MU = 0.25            # Adjustment parameter
    EPSILON_VALUES = np.linspace(0, 1, 20)  # Range of epsilon values (0 to 1 in 20 steps)

    # Analyze disconnected nodes for varying epsilon values
    disconnected_nodes = analyze_disconnected_nodes(N_RUNS, N_NODES, TIME_STEPS, MU, EPSILON_VALUES)

    # Plot the results
    plot_disconnected_nodes(EPSILON_VALUES, disconnected_nodes)
