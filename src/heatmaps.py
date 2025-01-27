import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_heatmap(file_path, image_title, parameter, reverse_columns = True):
    """
    Function to generate a heatmap from a CSV file and save it as an image.
    
    Args:
        file_path (str) : Path to the CSV file containing the data.
        image_title (str) : Desired title of the generated image.
        parameter (str) : What is the parameter varied in the matrix.
            This is also a title for the legend on the right-hand side of the heatmap. 
        reverse_columns (bool) : If True the order of columns are reversed
            to make the plot look like the the plot in the paper. 
    """
    # Load data from the CSV file
    data = pd.read_csv(file_path, index_col=0)
    if reverse_columns:
        data = data.iloc[::-1]

    # Plot a heatmap
    plt.figure(figsize=(16, 14)) 
    fig = sns.heatmap(data, annot=False, cmap='magma', cbar_kws={'label': parameter})

    plt.title(image_title, fontsize=20, pad=20)
    plt.xlabel('Mu Values', labelpad = 9, fontsize=16)
    plt.ylabel('Epsilon Values', labelpad = 9, fontsize=16)
    cbar = fig.collections[0].colorbar
    cbar.set_label(parameter, fontsize=16)

    # Save the heatmap
    plt.savefig(image_title, dpi=300)

    print("Heatmap saved")
