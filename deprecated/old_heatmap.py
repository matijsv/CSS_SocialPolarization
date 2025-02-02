

import csv
import pandas as pd
import numpy as np
from opynions.analysis.modularity import analyze_modularity
from opynions.analysis.similarity import analyze_neighbor_similarity
from opynions.analysis.isolation import analyze_disconnected_nodes

def opinion_matrix_experiment(n_runs, n_nodes, time_steps, mu_values, epsilon_values, output_file):
    """
    Investigates the average neighbor similarity by varying both epsilon and mu.
    Saves results as a 51x51 matrix to a CSV file.

    Args:
        n_runs (int): Number of simulation runs per parameter combination.
        n_nodes (int): Number of nodes in the graph.
        time_steps (int): Number of time steps for each simulation.
        mu_values (list or np.ndarray): Values of mu to investigate.
        epsilon_values (list or np.ndarray): Values of epsilon to investigate.
        output_file (str): File path to save the CSV results.
    """
    results_matrix = np.zeros((len(mu_values), len(epsilon_values)))  # Initialize matrix

    for i, epsilon in enumerate(epsilon_values):  # Outer loop: epsilon (horizontal)
        for j, mu in enumerate(mu_values):       # Inner loop: mu (vertical)
            print(f"Running simulation for epsilon={epsilon:.3f}, mu={mu:.3f}")
            # Analyze neighbor similarity
            avg_similarity = analyze_neighbor_similarity(n_runs, n_nodes, time_steps, mu, [epsilon])[0]
            results_matrix[j, i] = avg_similarity  # Store result in matrix

    # Save results to CSV
    df = pd.DataFrame(results_matrix, index=mu_values, columns=epsilon_values)
    df.to_csv(output_file)
    print(f"Results saved to {output_file}")
    


#Func for generating the heatmap
def generate_modularity_matrix(n_runs, n_nodes, time_steps, epsilon_range, mu_range, output_file):
    """
    Generates a 51x51 matrix of average modularity values for combinations of epsilon and mu,
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
        print(f"Analyzing modularity for epsilon = {epsilon:.3f}")

        for mu in mu_values:
            print(f"  Analyzing modularity for mu = {mu:.3f}")

            # Analyze modularity for the given epsilon and mu
            avg_modularities = analyze_modularity(n_runs, n_nodes, time_steps, mu, [epsilon])
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



""" ######## EXPERIMENT 6 #########
#generating data to heatmap - variance 

variance_matrix = [] 

epsilon_values = np.linspace(0, 0.5, 51)
miu_values = np.linspace(0, 0.5, 51)

for j in epsilon_values:
    variance_values = []
    for i in miu_values:
        var = distribution.opinions_variance(5, 2000, 10, j, i) 
        variance_values.append(var)
    variance_matrix.append(variance_values)

variance_matrix = np.array(variance_matrix)

#Saving to Data Frame 
df = pd.DataFrame(
    variance_matrix,
    index=[f"{epsilon:.2f}" for epsilon in epsilon_values],  # Rows - epsilon values
    columns=[f"{miu:.2f}" for miu in miu_values]  # Columns - miu values
)
df.index.name = "epsilon/mu"

# Saving to CSV
filename = "variance_heatmap_data.csv"
df.to_csv(filename)

print(f"Data saved to {filename}") """