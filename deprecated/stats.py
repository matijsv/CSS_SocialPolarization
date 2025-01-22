from matplotlib import pyplot as plt
from simulation import run_sim
import networkx as nx
from scipy.signal import find_peaks
import numpy as np

def plot_graphs(graphs, show=True):
    '''Plots a list of graphs'''
    
    for g in graphs:
        opinions = nx.get_node_attributes(g, 'opinion')
        pos = nx.spring_layout(g)
            
        fig, ax = plt.subplots(figsize=(8, 8))
            
        # Draw nodes with color based on opinion
        nx.draw_networkx_nodes(g, pos, node_color=list(opinions.values()), cmap=plt.cm.viridis, node_size=10)
        nx.draw_networkx_edges(g, pos, alpha=0.3)
            
        fig.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), ax=ax, label='Opinion')    
    if show:
        plt.show()
    
def run_stats(N_Nodes, T, N_Runs, epsilon, mu):
    all_histograms = []
    all_opinions = []
    for _ in range(N_Runs):
        g, g_init = run_sim(N_Nodes, T, epsilon=epsilon, mu=mu, plot=False, progress_bar=True)
        if N_Runs == 1:
            plot_graphs([g, g_init], show=False)
        opinions = nx.get_node_attributes(g, 'opinion').values()
        all_opinions.extend(opinions)
        # Create a histogram for the current run
        hist, bin_edges = np.histogram(list(opinions), bins=100, range=(0, 1))
        
        # Store the histogram
        all_histograms.append(hist)

    # Average the histograms & count the number of peaks
    average_histogram = np.mean(all_histograms, axis=0)
    peaks, peak_index = find_peaks(average_histogram, distance=10)
    num_peaks = len(peaks)
    
    # MAKE ALL_OPINIONS AN ARRAY OF ARRAYS
    return num_peaks, all_opinions, g

num_peaks, all_opinions, g = run_stats(2000, 100, 1, 0.1, 0.05, 'RUCM')
print(f'Number of peaks in the averaged histogram: {num_peaks}')
    

# Plot the distribution of opinions
plt.figure(figsize=(8, 8))
plt.hist(all_opinions, bins=100, range=(0,1), color='blue', edgecolor='black',density=True)
plt.xlim(0, 1)
plt.title('Distribution of Opinions')
plt.xlabel('Opinion')
plt.ylabel('Frequency')
plt.show()