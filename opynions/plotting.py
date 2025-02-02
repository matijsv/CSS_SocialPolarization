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


def plot_heatmap(file_path, image_title, reverse_columns=True):
    """
    Function to generate a heatmap from a CSV file and save it as an image.
    
    Args:
        file_path (str) : Path to the CSV file containing the data.
        image_title (str) : Desired title of the generated image.
        reverse_columns (bool) : If True the order of columns are reversed
            to make the plot look like the plot in the paper. 
    """
    # Load data from the CSV file
    data = pd.read_csv(file_path, index_col=0)
    
    # Flip the axes of the data
    if reverse_columns:
        data = data.iloc[::-1]
    
    # Plot a heatmap
    plt.figure(figsize=(16, 14)) 
    plt.minorticks_off()
    plt.minorticks_off()
    plt.tick_params(labelsize=20)
    fig = sns.heatmap(data, annot=False, cmap='magma')#, cbar_kws={'label': parameter})

    plt.title(image_title, fontsize=48, pad=60)
    plt.xlabel('Mu', labelpad=27, fontsize=30)
    plt.ylabel('Epsilon', labelpad=27, fontsize=30)
    
    cbar = fig.collections[0].colorbar
    cbar.ax.tick_params(labelsize=30)  # Increase colorbar tick label size
    

    # Save the heatmap
    plt.savefig(image_title, dpi=300)

    print("Heatmap saved")


def dicts_to_list_of_lists(dict_list):
    """
    Function to convert a list of dictionaries to a list of lists and a list of keys.
    
    Args:
        dict_list (list) : List of dictionaries with the same keys.
        
    Returns:
        tuple : A tuple containing a list of lists where each sublist contains the values corresponding to each key,
                and a list of keys in the order they appear in the output list.
    """
    if not dict_list:
        return [], []

    keys = list(dict_list[0].keys())
    result = {key: [] for key in keys}

    for d in dict_list:
        for key in keys:
            result[key].append(d[key])

    return [result[key] for key in keys], keys

def save_sublists_to_csv(data, keys, file_path):
    """
    Function to save a list of lists to a CSV file with columns labeled by keys.
    
    Args:
        data (list of lists) : List of lists where each sublist contains data for one column.
        keys (list of str) : List of keys to be used as column headers.
        file_path (str) : Path to the CSV file to save the data.
    """
    # Transpose the data to match the structure of a DataFrame
    data_transposed = list(zip(*data))
    
    # Create a DataFrame from the transposed data
    df = pd.DataFrame(data_transposed, columns=keys)
    
    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False)
    
    print(f"Data saved to {file_path}")


def create_subplots(data, x_index, titles, x_label, y_labels):
    """
    Function to create subplots from a list of lists.
    
    Args:
        data (list of lists) : List of lists where each sublist contains data for one subplot.
        x_index (int) : Index of the sublist to be used as the x-axis for all subplots.
        titles (list of str) : Titles for each subplot.
        x_label (str) : Label for the x-axis.
        y_labels (list of str) : Labels for the y-axes of each subplot.
    """
    num_plots = len(data) - 1
    x_data = data[x_index]
    
    fig, axes = plt.subplots(1, num_plots, figsize=(4 * num_plots, 4))
    
    if num_plots == 1:
        axes = [axes]
    
    for i, ax in enumerate(axes):
        if i == x_index:
            continue
        ax.plot(x_data, data[i])
        ax.set_title(titles[i], fontsize=16)
        ax.set_xlabel(x_label, fontsize=14)
        ax.set_ylabel(y_labels[i], fontsize=14)
    
    # Save the plots
    plt.savefig('full_analysis_lines_mu36', dpi=300)
    
    plt.tight_layout()
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