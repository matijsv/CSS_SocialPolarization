'''Functions for analysis of disconnected nodes in the network. '''

import csv
import numpy as np
import networkx as nx
from src.core.utils import get_graphs

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

#Func for generating the heatmap
def generate_disconnected_nodes_matrix(n_runs, n_nodes, time_steps,
                                       epsilon_range, mu_range, output_file):
    """
    Generates a 51x51 matrix of average disconnected nodes for combinations of epsilon and mu,
    and saves the result to a CSV file.

    Args:
        n_runs (int): Number of simulations per parameter combination.
        n_nodes (int): Number of nodes in each graph.
        time_steps (int): Number of time steps.
        epsilon_range (tuple): Range of epsilon values (start, end, steps).
        mu_range (tuple): Range of mu values (start, end, steps).
        output_file (str): File path to save the resulting CSV file.
    """
    # Generate 51 values for epsilon and mu
    epsilon_values = np.linspace(epsilon_range[0], epsilon_range[1], epsilon_range[2])
    mu_values = np.linspace(mu_range[0], mu_range[1], mu_range[2])

    # Initialize an empty matrix
    matrix = []

    for epsilon in epsilon_values:
        row = []
        print(f"Analyzing for epsilon = {epsilon:.3f}")

        for mu in mu_values:
            print(f"  Analyzing for mu = {mu:.3f}")
  
            # Analyze disconnected nodes for the given epsilon and mu
            avg_disconnected_nodes = analyze_disconnected_nodes(n_runs, n_nodes, time_steps, mu, [epsilon])
            row.append(avg_disconnected_nodes[0])  # Extract single result for epsilon
        
        # Append the row to the matrix
        matrix.append(row)
    
    # Save the matrix to a CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["epsilon \\ mu"] + list(mu_values))  # Header row
        for i, epsilon in enumerate(epsilon_values):
            writer.writerow([epsilon] + matrix[i])
    
    print(f"Matrix saved to {output_file}")


