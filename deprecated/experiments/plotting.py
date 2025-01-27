import matplotlib as plt
import networkx as nx

def plot_communities(epsilon_values, communities):
    """
    Plots the number of communities as a function of epsilon.

    Args:
        epsilon_values (list or numpy.ndarray): Range of epsilon values.
        communities (list): Average number of communities for each epsilon value.
    """
    plt.figure()
    plt.plot(epsilon_values, communities, marker='o', color='b')
    plt.title("Number of Communities vs. Epsilon")
    plt.xlabel("Epsilon")
    plt.ylabel("Number of Communities")
    plt.grid(True)
    plt.show()
    
def plot_modularity(epsilon_values, modularities):
    """
    Plots the modularity as a function of epsilon.

    Args:
        epsilon_values (list or numpy.ndarray): Epsilon values (x-axis).
        modularities (list): Modularity values (y-axis).
    """
    plt.figure(figsize=(10, 6))
    plt.plot(epsilon_values, modularities, marker='o', linestyle='-', color='g', label='Modularity')
    plt.xlabel('Epsilon')
    plt.ylabel('Modularity')
    plt.title('Modularity vs Epsilon')
    plt.grid(True)
    plt.legend()
    plt.show()
    
def plot_disconnected_nodes(epsilon_values, disconnected_nodes):
    """
    Plots the number of disconnected nodes as a function of epsilon.

    Args:
        epsilon_values (list or numpy.ndarray): Epsilon values (x-axis).
        disconnected_nodes (list): Number of disconnected nodes (y-axis).
    """
    plt.figure(figsize=(10, 6))
    plt.plot(epsilon_values, disconnected_nodes, marker='o', linestyle='-', color='b', label='Disconnected Nodes')
    plt.xlabel('Epsilon')
    plt.ylabel('Number of Disconnected Nodes')
    plt.title('Disconnected Nodes vs Epsilon')
    plt.grid(True)
    plt.legend()
    plt.show()
    
def plot_neighbor_similarity(epsilon_values, similarities):
    """
    Plots the neighbor similarity as a function of epsilon.

    Args:
        epsilon_values (list or numpy.ndarray): Epsilon values (x-axis).
        similarities (list): Neighbor similarity values (y-axis).
    """
    plt.figure(figsize=(10, 6))
    plt.plot(epsilon_values, similarities, marker='o', linestyle='-', color='b', label='Neighbor Similarity')
    plt.xlabel('Epsilon')
    plt.ylabel('Average Neighbor Similarity')
    plt.title('Neighbor Similarity vs Epsilon')
    plt.grid(True)
    plt.legend()
    plt.show()
    
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