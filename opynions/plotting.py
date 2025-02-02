import pandas as pd
import seaborn as sns
import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(g, include_colorbar=True, exclude_isolates=False, file_path='graph_plot.png'):
    """
    Plots the graph with nodes colored by opinion and saves it to a file.

    Args:
        g (networkx.Graph): Graph to plot.
        include_colorbar (bool): Whether to include the colorbar in the plot.
        exclude_isolates (bool): Whether to exclude isolated nodes from the plot.
        file_path (str): Path to save the plot image.
    """
    if g.number_of_nodes() > 0:
        if exclude_isolates:
            g = g.copy()
            isolates = list(nx.isolates(g))
            g.remove_nodes_from(isolates)
        
        opinions = nx.get_node_attributes(g, 'opinion')
        pos = nx.spring_layout(g)

        fig, ax = plt.subplots(figsize=(8, 8))

        # Draw nodes with color based on opinion
        nx.draw_networkx_nodes(g, pos, node_color=list(opinions.values()), cmap=plt.cm.viridis, node_size=10)
        nx.draw_networkx_edges(g, pos, alpha=0.3)

        if include_colorbar:
            cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), ax=ax, label='Opinion')
            cbar.ax.yaxis.label.set_size(30)  # Increase colorbar label size
            cbar.ax.tick_params(labelsize=30)  # Increase colorbar label size
        
        plt.savefig(file_path, dpi=300)
        plt.show()
    
def create_heatmap_from_csv(file_path, value_column, x_coord_column, y_coord_column, image_title):
    """
    Function to create a heatmap from a CSV file with user-defined columns for values and coordinates.
    
    Args:
        file_path (str) : Path to the CSV file containing the data.
        value_column (str) : Name of the column to be used for heatmap values.
        x_coord_column (str) : Name of the column to be used for x-axis coordinates.
        y_coord_column (str) : Name of the column to be used for y-axis coordinates.
        image_title (str) : Desired title of the generated image.
        parameter (str) : Title for the legend on the right-hand side of the heatmap.
    """
    # Load data from the CSV file
    data = pd.read_csv(file_path)
    
    # Pivot the data to create a matrix for the heatmap
    heatmap_data = data.pivot(index=y_coord_column, columns=x_coord_column, values=value_column)
    
    # Reverse the y-axis
    heatmap_data = heatmap_data.iloc[::-1]
    
    # Plot a heatmap
    plt.figure(figsize=(16, 14)) 
    plt.minorticks_off()
    plt.minorticks_off()
    plt.tick_params(labelsize=20)
    fig = sns.heatmap(heatmap_data, annot=False, cmap='magma')#, cbar_kws={'label': parameter})

    plt.title(image_title, fontsize=48, pad=60)
    plt.xlabel(x_coord_column, labelpad=27, fontsize=30)
    plt.ylabel(y_coord_column, labelpad=27, fontsize=30)
    
    cbar = fig.collections[0].colorbar
    cbar.ax.tick_params(labelsize=30)  # Increase colorbar tick label size
    

    # Save the heatmap
    plt.savefig(image_title, dpi=300)

    print("Heatmap saved")