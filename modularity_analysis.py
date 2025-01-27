import matplotlib.pyplot as plt
import numpy as np
import csv
import networkx as nx
from utils import get_graphs
from networkx.algorithms.community import modularity
from networkx.algorithms.community import greedy_modularity_communities 

def calculate_modularity(graph, exclude_isolates=True):
    """
    Calculates the modularity of a graph based on community detection.

    Args:
        graph (networkx.Graph): The graph for which to calculate modularity.
        exclude_isolates (boolean): Whether to exclude isolated nodes.
    Returns:
        float: The modularity of the graph.
    """
    if exclude_isolates:
        graph.remove_nodes_from(list(nx.isolates(graph)))
    # Use the greedy modularity communities detection algorithm
    communities = greedy_modularity_communities(graph)
    # Calculate modularity
    mod_value = modularity(graph, communities)
    return mod_value

def analyze_modularity(N_runs, N_nodes, time_steps, mu, epsilon_values):
    """
    Analyzes and calculates the average modularity of graphs for a range of epsilon values.

    Args:
        N_runs (int): Number of runs for each epsilon value.
        N_nodes (int): Number of nodes in the graph.
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
        final_graphs, _ = get_graphs(N_runs, N_nodes, time_steps, epsilon, mu)

        # Calculate modularity for each graph and accumulate the total
        for graph in final_graphs:
            total_modularity += calculate_modularity(graph)
        
        # Compute the average modularity for this epsilon
        avg_modularity = total_modularity / N_runs
        avg_modularities.append(avg_modularity)
    
    return avg_modularities

def plot_modularity(epsilon_values, modularities):
    """
    Plots the modularity as a function of epsilon.

    Args:
        epsilon_values (list or numpy.ndarray): Epsilon values (x-axis).
        modularities (list): Modularity values (y-axis).
    """
    plt.figure(figsize=(10, 6))
    plt.plot(epsilon_values, modularities, marker='o', linestyle='-', color='g', label='Modularity')
    plt.xlabel('Epsilon')
    plt.ylabel('Modularity')
    plt.title('Modularity vs Epsilon')
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

    # Analyze modularity for varying epsilon values
    modularities = analyze_modularity(N_RUNS, N_NODES, TIME_STEPS, MU, EPSILON_VALUES)

    # Plot the results
    plot_modularity(EPSILON_VALUES, modularities)

#function to generate heatmaps
def generate_modularity_matrix(N_runs, N_nodes, time_steps, epsilon_range, mu_range, output_file):
    """
    Generates a 51x51 matrix of average modularity values for combinations of epsilon and mu,
    and saves the result to a CSV file.

    Args:
        N_runs (int): Number of simulations per parameter combination.
        N_nodes (int): Number of nodes in each graph.
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
        print(f"Analyzing modularity for epsilon = {epsilon:.3f}")
        
        for mu in mu_values:
            print(f"  Analyzing modularity for mu = {mu:.3f}")
            
            # Analyze modularity for the given epsilon and mu
            avg_modularities = analyze_modularity(N_runs, N_nodes, time_steps, mu, [epsilon])
            row.append(avg_modularities[0])  # Extract single result for epsilon
        
        # Append the row to the matrix
        matrix.append(row)
    
    # Save the matrix to a CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["epsilon \\ mu"] + list(mu_values))  # Header row
        for i, epsilon in enumerate(epsilon_values):
            writer.writerow([epsilon] + matrix[i])
    
    print(f"Matrix saved to {output_file}")

# usage
if __name__ == "__main__":
    # Parameters
    N_RUNS = 5           # Number of simulations per parameter combination
    N_NODES = 2000       # Number of nodes in each graph
    TIME_STEPS = 100     # Number of time steps
    EPSILON_RANGE = (0, 0.5, 51)  # Epsilon values from 0 to 0.5 (51 steps)
    MU_RANGE = (0, 0.5, 51)       # Mu values from 0 to 0.5 (51 steps)
    OUTPUT_FILE = "modularity_matrix.csv"

    # Generate the matrix and save to file
    generate_modularity_matrix(N_RUNS, N_NODES, TIME_STEPS, EPSILON_RANGE, MU_RANGE, OUTPUT_FILE)


