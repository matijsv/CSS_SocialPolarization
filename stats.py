from matplotlib import pyplot as plt
from main import run_sim
import networkx as nx
from scipy.signal import find_peaks
import numpy as np

N_RUNS = 5
all_histograms = []
all_opinions = []
for _ in range(N_RUNS):
    g = run_sim(2000, 100, epsilon=0.25, mu=0.45, type='RUCM', plot=False, progress_bar=True)
    opinions = nx.get_node_attributes(g, 'opinion').values()
    all_opinions.extend(opinions)
    # Create a histogram for the current run
    hist, bin_edges = np.histogram(list(opinions), bins=100, range=(0, 1))
    
    # Store the histogram
    all_histograms.append(hist)

# Average the histograms
average_histogram = np.mean(all_histograms, axis=0)

# Find peaks in the averaged histogram
peaks, _ = find_peaks(average_histogram, distance=10, height=20)

# Count the number of peaks
num_peaks = len(peaks)

print(f'Number of peaks in the averaged histogram: {num_peaks}')
    

# Plot the distribution of opinions
plt.figure(figsize=(8, 8))
plt.hist(all_opinions, bins=100, range=(0,1), color='blue', edgecolor='black',density=True)
plt.xlim(0, 1)
plt.title('Distribution of Opinions')
plt.xlabel('Opinion')
plt.ylabel('Frequency')
plt.show()