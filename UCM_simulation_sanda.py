import numpy as np
import networkx as nx
import random
import matplotlib.pyplot as plt

"""just a random network to use for this simulation"""

def initialize_network(num_nodes):  
    """Initialize a scale-free network and assign random opinions to each node."""
    G = nx.barabasi_albert_graph(num_nodes, m=2)  # Scale-free network
    opinions = np.random.uniform(0, 1, num_nodes)  # Random opinions in [0, 1]
    nx.set_node_attributes(G, {i: opinions[i] for i in range(num_nodes)}, 'opinion')
    return G

"""Trying to visualize the network first"""
def visualize_network(G):
    """Visualize the network with node colors based on opinions."""
    # Get opinions for each node to use as colors
    opinions = nx.get_node_attributes(G, 'opinion')
    node_colors = [opinions[node] for node in G.nodes]

    # Draw the network
    plt.figure(figsize=(10, 10))
    nx.draw(
        G,
        pos=nx.spring_layout(G),  # Layout algorithm for visualization
        node_color=node_colors,  # Use opinions to color nodes
        cmap=plt.cm.viridis,     # Color map
        with_labels=False,       # No labels for simplicity
        node_size=50,            # Adjust node size
        edge_color='gray',       # Set edge color
        alpha=0.7                # Transparency for edges
    )
    plt.title("Scale-Free Network with Node Opinions")
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), label='Opinion')
    plt.show()

# Initialize the network
G = initialize_network(100)  # 100 nodes for example

# Visualize the network
visualize_network(G)


"""applpy the math formulas"""

def update_opinions(G, mu, epsilon):
    """Update opinions according to the Unbounded Confidence Model."""
    nodes = list(G.nodes())
    random.shuffle(nodes)  # Shuffle to ensure random pair selection

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            xi = G.nodes[nodes[i]]['opinion']
            xj = G.nodes[nodes[j]]['opinion']
            distance = abs(xi - xj)
            if not np.isfinite(distance):
                continue  # Skip invalid pairs

             # Update opinions if concordant
            if distance < epsilon:
             G.nodes[i]['opinion'] = np.clip(xi + mu * (xj - xi), 0, 1)
             G.nodes[j]['opinion'] = np.clip(xj + mu * (xi - xj), 0, 1)
            # Update opinions if discordant
            else:
             tau = distance - np.sign(distance - epsilon)
             G.nodes[i]['opinion'] = np.clip(xi - mu * (tau - np.sign(tau)), 0, 1)
             G.nodes[j]['opinion'] = np.clip(xj - mu * (tau - np.sign(tau)), 0, 1)

        """ if distance < epsilon:  # Concordant opinions
                G.nodes[nodes[i]]['opinion'] = xi + mu * (xj - xi)
                G.nodes[nodes[j]]['opinion'] = xj + mu * (xi - xj)

            elif distance >= epsilon:  # Discordant opinions
                tau = distance - np.sign(distance - epsilon)
                G.nodes[nodes[i]]['opinion'] = xi - mu * (tau - np.sign(tau))
                G.nodes[nodes[j]]['opinion'] = xj - mu * (tau - np.sign(tau)) """


def simulate_ucm(num_nodes, mu, epsilon, num_steps):
    """Simulate the Unbounded Confidence Model."""
    G = initialize_network(num_nodes)
    opinions_over_time = []

    for t in range(num_steps):
        update_opinions(G, mu, epsilon)
        opinions = [G.nodes[node]['opinion'] for node in G.nodes()]
        opinions_over_time.append(opinions)

    return opinions_over_time

# Simulation Parameters
num_nodes = 2000
mu = 0.1  # Convergence parameter
epsilon = 0.1  # Tolerance threshold
num_steps = 100

# Try to simulate
opinions_over_time = simulate_ucm(num_nodes, mu, epsilon, num_steps)

# Visualize final opinions
final_opinions = opinions_over_time[-1]
plt.hist(final_opinions, bins=100, color='skyblue', edgecolor='black')
plt.xlabel('Opinion')
plt.ylabel('Frequency')
plt.title('Final Distribution of Opinions')
plt.show()
