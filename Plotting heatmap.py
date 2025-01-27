import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_heatmap(file_path, image_title):
    """
    Function to generate a heatmap from a CSV file and save it as an image.
    
    Args:
        file_path (str) : Path to the CSV file containing the data.
        image_title (str) : Desired title of the generated image. 
    """
    # Load data from the CSV file
    data = pd.read_csv(file_path, index_col=0)

    # Plot a heatmap
    plt.figure(figsize=(16, 14)) 
    fig = sns.heatmap(data, annot=False, cmap='magma', cbar_kws={'label': 'Variance'})

    
    plt.title(image_title, fontsize=20, pad=20)
    plt.xlabel('Mu Values', labelpad = 9, fontsize=16)
    plt.ylabel('Epsilon Values', labelpad = 9, fontsize=16)
    cbar = fig.collections[0].colorbar
    cbar.set_label('Variance', fontsize=16)
    
    # Save the heatmap
    plt.savefig("heatmap.png", dpi=300)

    print(f"Heatmap saved")