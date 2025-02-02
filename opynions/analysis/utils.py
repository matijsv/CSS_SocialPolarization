'''Utility functions for data handling and plotting'''

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns

def list_of_dicts_to_csv(dict_list, file_path):
    """
    Function to convert a list of dictionaries to a list of lists and save it to a CSV file.
    
    Args:
        dict_list (list) : List of dictionaries with the same keys.
        file_path (str) : Path to the CSV file to save the data.
        
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

    data = [result[key] for key in keys]

    # Transpose the data to match the structure of a DataFrame
    data_transposed = list(zip(*data))
    
    # Create a DataFrame from the transposed data
    df = pd.DataFrame(data_transposed, columns=keys)
    
    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False)

    return data, keys


def create_heatmap_from_csv(file_path, value_column, x_coord_column, y_coord_column,
                            save=False, image_path='Heatmap.png',):
    """
    Function to create a heatmap from a CSV file with user-defined columns for values and coordinates.

    Args:
        file_path (str) : Path to the CSV file containing the data.
        value_column (str) : Name of the column to be used for heatmap values, is also the title.
        x_coord_column (str) : Name of the column to be used for x-axis coordinates.
        y_coord_column (str) : Name of the column to be used for y-axis coordinates.
        save (bool, optional) : whether to save the image or not. Default False
        image_path (str, optional) : OPTIONAL desired path of the generated image. Default 'Heatmap.png'.
    """
    # Load data from the CSV file
    data = pd.read_csv(file_path)

    # Pivot the data to create a matrix for the heatmap
    heatmap_data = data.pivot(index=y_coord_column, columns=x_coord_column, values=value_column)

    # Reverse the y-axis
    heatmap_data = heatmap_data.iloc[::-1]

    # Plot a heatmap
    plt.figure(figsize=(4, 4))
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.1f}'))
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1f}'))
    plt.minorticks_off()
    plt.minorticks_off()
    plt.tick_params(labelsize=10)
    
    fig = sns.heatmap(heatmap_data, annot=False, cmap='magma')#, cbar_kws={'label': parameter})

    plt.title(value_column, fontsize=20, pad=30)
    plt.xlabel(x_coord_column, labelpad=10, fontsize=10)
    plt.ylabel(y_coord_column, labelpad=10, fontsize=10)

    cbar = fig.collections[0].colorbar
    cbar.ax.tick_params(labelsize=10)  # Increase colorbar tick label size

    # Save the heatmap
    if save:
        plt.savefig(image_path, dpi=300)
        print("Heatmap saved")    


def plot_graph(g, include_colorbar=True, exclude_isolates=False, save_file=False, file_path='graph_plot.png'):
    """
    Plots the graph with nodes colored by opinion and saves it to a file.

    Args:
        g (networkx.Graph): Graph to plot.
        include_colorbar (bool, optional): Whether to include the colorbar in the plot. Default True.
        exclude_isolates (bool, optional): Whether to exclude isolated nodes from the plot. Default False.
        save_file (bool, optional): Whether to save the image file. Default False.
        file_path (str, optional): Path to save the plot image. Default 'graph_plot.png'.
    """
    if g.number_of_nodes() > 0:
        if exclude_isolates:
            g = g.copy()
            isolates = list(nx.isolates(g))
            g.remove_nodes_from(isolates)

        opinions = nx.get_node_attributes(g, 'opinion')
        pos = nx.spring_layout(g)

        fig, ax = plt.subplots(figsize=(4, 4))

        # Draw nodes with color based on opinion
        nx.draw_networkx_nodes(g, pos, node_color=list(opinions.values()), cmap=plt.cm.viridis, node_size=5)
        nx.draw_networkx_edges(g, pos, alpha=0.3)

        if include_colorbar:
            cbar = fig.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), ax=ax, label='Opinion')
            cbar.ax.yaxis.label.set_size(10)  # Increase colorbar label size
            cbar.ax.tick_params(labelsize=10)  # Increase colorbar label size
        if save_file:
            plt.savefig(file_path, dpi=300)
        plt.show()

def plot_subplots_from_csv(csv_file, x_axis_column, save_file=False, file_path='sliceplots.png'):
    """
    Plots subplots from a CSV file with metrics against a specified x-axis column.
    
    Args:
    csv_file (str): Path to the CSV file containing the data.
    x_axis_column (str): The column to be used as the x-axis. Must be either 'epsilon' or 'mu'.
    save_file (bool, optional): If True, saves the plot to a file. Default is False.
    file_path (str, optional): The file path to save the plot if save_file is True. Default is 'sliceplots.png'.
    
    Raises:
    ValueError: If x_axis_column is not 'epsilon' or 'mu'.
    
    Returns:
    None
    """
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Check if the x_axis_column is valid
    if x_axis_column not in ['epsilon', 'mu']:
        raise ValueError("x_axis_column must be either 'epsilon' or 'mu'")
    
    # Drop the column that is not used
    columns_to_drop = [col for col in ['epsilon', 'mu'] if col != x_axis_column]
    set_parameter_value = df[columns_to_drop].iloc[0, 0]
    df = df.drop(columns=columns_to_drop)
    
    # Create subplots
    num_plots = len(df.columns) - 1
    fig, axes = plt.subplots(1, num_plots, figsize=(3*num_plots, 3))
    fig.suptitle(f'Metrics vs {x_axis_column}. With {columns_to_drop[0]} = {set_parameter_value}')
    # Plot each column
    for i, column in enumerate(df.columns):
        if column != x_axis_column:
            axes[i].plot(df[x_axis_column], df[column])
            axes[i].set_title(f'{column}')
            axes[i].set_xlabel(x_axis_column)
            axes[i].set_ylabel(column)
    
    plt.tight_layout()
    if save_file:
        plt.savefig(file_path, dpi=300)
    

def plot_opinion_distribution(g, save_file=False, file_path='opinion_distribution.png'):
    """
    Plots the opinion distribution histogram from a graph and (optionally) saves it to a file.

    Args:
        g (networkx.Graph): Graph with 'opinion' attribute for nodes.
        save_file (bool, optional): Whether to save the histogram to a file. Default False.
        file_path (str, optional): Path to save the histogram image. Default 'opinion_distribution.png'.
    """
    opinions = nx.get_node_attributes(g, 'opinion').values()
    
    plt.figure(figsize=(2, 1))
    plt.hist(opinions, bins=100, color='blue', edgecolor='black')
    plt.title('Opinion Distribution')
    plt.xlabel('Opinion')
    plt.ylabel('Frequency')
    
    if save_file:
        plt.savefig(file_path, dpi=300)
        print(f"Opinion distribution histogram saved to {file_path}")
    
    plt.show()