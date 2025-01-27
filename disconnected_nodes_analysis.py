import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import csv
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


#Code tro generate the heatmap

def generate_disconnected_nodes_matrix(N_runs, N_nodes, time_steps, epsilon_range, mu_range, output_file):
    """
    Generates a 51x51 matrix of average disconnected nodes for combinations of epsilon and mu,
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
        print(f"Analyzing for epsilon = {epsilon:.3f}")
        
        for mu in mu_values:
            print(f"  Analyzing for mu = {mu:.3f}")
            
            # Analyze disconnected nodes for the given epsilon and mu
            avg_disconnected_nodes = analyze_disconnected_nodes(N_runs, N_nodes, time_steps, mu, [epsilon])
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

#usage
if __name__ == "__main__":
    # Parameters
    N_RUNS = 5           # Number of simulations per parameter combination
    N_NODES = 2000       # Number of nodes in each graph
    TIME_STEPS = 100     # Number of time steps
    EPSILON_RANGE = (0, 0.5, 51)  # Epsilon values from 0 to 0.5 (51 steps)
    MU_RANGE = (0, 0.5, 51)       # Mu values from 0 to 0.5 (51 steps)
    OUTPUT_FILE = "disconnected_nodes_matrix.csv"

    # Generate the matrix and save to file
    generate_disconnected_nodes_matrix(N_RUNS, N_NODES, TIME_STEPS, EPSILON_RANGE, MU_RANGE, OUTPUT_FILE)


