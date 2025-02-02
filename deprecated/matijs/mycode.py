# from src.heatmaps import plot_heatmap
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
folder_path = 'raw_data/'   # Path to the folder containing the CSV files

def plot_heatmaps(folder_path, image_title, parameters, reverse_columns=True):
    """
    Function to generate heatmaps from all CSV files in a folder and save them as subplots in a single image.
    
    Args:
        folder_path (str) : Path to the folder containing the CSV files.
        image_title (str) : Desired title of the generated image.
        parameters (list) : List of strings, each string is a parameter varied in the matrix.
            Each string is also a title for the legend on the right-hand side of the heatmap. 
        reverse_columns (bool) : If True the order of columns are reversed
            to make the plot look like the plot in the paper. 
    """
    
    # Get list of all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    # Determine the number of rows and columns for subplots
    num_files = len(csv_files)
    num_cols = 2
    num_rows = (num_files + 1) // num_cols
    
    # Create a figure for subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(22, 14 * num_rows))
    axes = axes.flatten()
    
    for i, file_name in enumerate(csv_files):
        file_path = os.path.join(folder_path, file_name)
        
        # Load data from the CSV file
        data = pd.read_csv(file_path, index_col=0)
        if reverse_columns:
            data = data.iloc[::-1]
        
        # Plot a heatmap
        sns.heatmap(data, annot=False, cmap='magma', cbar_kws={'label': parameters[i]}, ax=axes[i])
        axes[i].set_title(file_name, fontsize=16, pad=10)
        axes[i].set_xlabel('Mu Values', labelpad=9, fontsize=12)
        axes[i].set_ylabel('Epsilon Values', labelpad=9, fontsize=12)
    
    # Adjust layout and save the figure
    plt.tight_layout()
    plt.suptitle(image_title, fontsize=20, y=1.02)
    plt.savefig(image_title, dpi=300)
    
    print("Heatmaps saved")

# plot_heatmaps(folder_path, 'heatmap_overview', ['Disconnecteds', 'Variance', 'Similarity'])

from opynions.core.utils import get_graphs
import networkx as nx

def plot_graph(g):
    """
    Plots the graph with nodes colored by opinion.

    Args:
        g (networkx.Graph): Graph to plot.
    """
    if g.number_of_nodes() > 0:
        opinions = nx.get_node_attributes(g, 'opinion')
        pos = nx.spring_layout(g)

        fig, ax = plt.subplots(figsize=(8, 8))

        # Draw nodes with color based on opinion
        nx.draw_networkx_nodes(g, pos, node_color=list(opinions.values()), cmap=plt.cm.viridis, node_size=10)
        nx.draw_networkx_edges(g, pos, alpha=0.3)

        fig.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), ax=ax, label='Opinion')
        plt.show()



#graph, _ = get_graphs(1, 2000, 100, epsilon, mu)
#plot_graph(graph[0])

from opynions.analysis.combined import combined_analysis

from opynions.analysis.multiprocessing import multiprocess_mod_comm_both, multiprocess_all_both
import time
import numpy as np
start_time = time.time()
print(combined_analysis(5, 2000, 100, epsilon, mu))
end_time = time.time()
print(f"Time taken single: {end_time - start_time} seconds")
#plot_graph(get_graphs(1, 2000, 100, epsilon, mu)[0][0])

start_time = time.time()
list_of_dicts = multiprocess_epsilon([0.8])
end_time = time.time()
print(f"Time taken multiprocessing single: {end_time - start_time} seconds")

from opynions.plotting import create_heatmap_from_csv, dicts_to_list_of_lists, save_sublists_to_csv, create_subplots

#start_time = time.time()
#epsilon_values = np.linspace(0,0.5,51) 
#mu_values = np.linspace(0,0.5,51)
#list_of_dicts = multiprocess_mod_comm_both(epsilon_values, mu_values)
#end_time = time.time()
#print(f"Time taken multiprocessing 8 vals: {end_time - start_time} seconds")
#print(f"Estimate time for completion of full 51x51 matrices: {((end_time - start_time)*(((51*51)/9)))/60/60} hours")
#print(f"Estimate time for completion of 100 datapoint lines: {((end_time - start_time)*(((100)/9)))/60/60} hours")
#list_of_lists, keys = dicts_to_list_of_lists(list_of_dicts)
#save_sublists_to_csv(list_of_lists, keys, f'raw_data/formod_comm_heatmaps.csv')

#create_subplots(list_of_lists,-1,keys[:-1],'epsilon',keys[:-1])


#create_heatmap_from_csv('raw_data/formod_comm_heatmaps.csv','avg_modularity','mu','epsilon','Modularity','Modularity')
#create_heatmap_from_csv('raw_data/formod_comm_heatmaps.csv','avg_num_communities','mu','epsilon','Number of communities','# Communities')

""" epsilon_values = np.linspace(0,0.5,10) 
mu_values = np.linspace(0,0.5,10)
list_of_dicts = multiprocess_all_both(epsilon_values, mu_values)

list_of_lists, keys = dicts_to_list_of_lists(list_of_dicts)
save_sublists_to_csv(list_of_lists, keys, f'raw_data/testing_all.csv')

create_heatmap_from_csv('raw_data/testing_all.csv','avg_similarity','mu','epsilon','Similarity','Similarity') """


epsilon = 0.1
mu = 0.05
# file_path = f'Figures/network_examples/g_e{int(epsilon*100)}_m{int(mu*100)}.png'
file_path = f'Figures/network_examples/FIRST_g_e12_m3.png'
plot_graph(get_graphs(1, 2000, 100, epsilon, mu)[0][0],True,True, file_path)