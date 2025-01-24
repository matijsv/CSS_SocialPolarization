import utils
import numpy as np
from scipy.signal import find_peaks

def opinions_variance(N_runs, N_nodes, time_steps, epsilon, mu):
    """
    Function to calculate variance of all opinions.

    Args:
        N_runs (int): The number of simulation runs.
        N_nodes (int): The number of nodes in the network.
        time_steps (int): The number of time steps to simulate.
        epsilon (float): Tolerance parameter (range: [0, 0.5]).
        mu (float): Convergence parameter (range: [0, 0.5]).
    
    Returns:
        float: The variance of opinions across all nodes and all runs.
    """

    #run the simulation
    all_opinions, _ = utils.get_opinion_hist(N_runs, N_nodes, time_steps, epsilon, mu, exclude_loners=False)

    #calculate variance from all opinions
    flattened_opinions = [opinion for run in all_opinions for opinion in run]
    variance = np.var(flattened_opinions)

    return(variance)

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


