'''Functions for analysis of opinion distribution in the network.'''

import numpy as np
from scipy.signal import find_peaks
from opynions.core.utils import get_opinion_hist

def opinions_variance(n_runs, n_nodes, time_steps, epsilon, mu):
    """
    Function to calculate variance of all opinions.

    Args:
        n_runs (int): The number of simulation runs.
        n_nodes (int): The number of nodes in the network.
        time_steps (int): The number of time steps to simulate.
        epsilon (float): Tolerance parameter (range: [0, 0.5]).
        mu (float): Convergence parameter (range: [0, 0.5]).
    
    Returns:
        float: The variance of opinions across all nodes and all runs.
    """

    #run the simulation
    all_opinions, _ , _ = get_opinion_hist(n_runs, n_nodes, time_steps, epsilon,
                                           mu, exclude_loners=False)

    #calculate variance from all opinions
    flattened_opinions = [opinion for run in all_opinions for opinion in run]
    variance = np.var(flattened_opinions)

    return variance

def count_peaks_in_histogram(average_histogram, threshold=100, distance=10):
    """
    Function to count the peaks in the average histogram of opinions.
    
    Parameters:
        average_histogram (list) : The average histogram of opinions.
        threshold (float) :  Minimum height for a peak to be considered.
        distance (int) :  Minimum number of bins between peaks.

    Returns:
        num_peaks (int) : The number of peaks in the histogram.
        peak_indices (list) : Indices of the peaks in the histogram.
    """
    peak_indices, _ = find_peaks(average_histogram, height=threshold, distance=distance)

    # Count the number of peaks
    num_peaks = len(peak_indices)

    return num_peaks


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