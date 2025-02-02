import matplotlib.pyplot as plt
import seaborn as sns 
import pandas as pd 
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