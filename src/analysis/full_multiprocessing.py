import networkx as nx
import numpy as np
import multiprocessing as mp
import matplotlib.pyplot as plt

def generate_random_network():
    # Generate a random network (Erdős-Rényi graph as an example)
    G = nx.barabasi_albert_graph(n=1000, m=2)
    return G

def analyze_network(G):
    # Analyze the network to find its degree distribution
    degree_sequence = [d for n, d in G.degree()]
    return degree_sequence

def worker(_):
    G = generate_random_network()
    degree_sequence = analyze_network(G)
    hist, _ = np.histogram(degree_sequence, bins=101)
    return hist

def main():
    num_networks = 2000
    num_workers = mp.cpu_count()

    with mp.Pool(num_workers) as pool:
        list_of_hists = pool.map(worker, range(num_networks))

    # Average the degree distributions
    average_degree_distribution = np.mean(list_of_hists, axis=0)

    print("Average Degree Distribution:", average_degree_distribution)

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.loglog(range(len(average_degree_distribution)), average_degree_distribution, color='blue', alpha=0.7)
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.title('Average Degree Distribution')
    plt.show()

if __name__ == "__main__":
    print(mp.cpu_count())
    main()
    
    
# SCHEME:
# WORKER RETURNS AN ARRAY INCLUDING 5 RUN-AVERAGED VARIANCE, SIMILARITY, DISCONNECTEDS, NUM COMMUNITIES and MODULARITY
# MAIN, FOR VALUES IN EPSILON COLLECTS ALL THE DATA AND CALCULATES AVERAGES

# SO WORKER NEEDS TO LOOP N-RUNS: 
# RUN SIMULATION (CREATE FINAL GRAPH OBJECT)
# CALL ANALYSIS FUNCTIONS (VARIANCE, SIMILARITY, DISCONNECTEDS, NUM COMMUNITIES, MODULARITY)
# AGREGATE INTO AN ARRAY AND RETURN

# FOR LATER POSSIBLE HEATMAP CREATION LOOK INTO ITERTOOLS.PRODUCT FOR EPSILON AND MU VALUES

# As stated in the documentation, 
# concurrent.futures.ProcessPoolExecutor is a wrapper around a multiprocessing.Pool.
# As such, the same limitations of multiprocessing apply (e.g. objects need to be pickleable).
# https://stackoverflow.com/questions/38311431/concurrent-futures-processpoolexecutor-vs-multiprocessing-pool-pool

# make num runs a (i think best global) variable