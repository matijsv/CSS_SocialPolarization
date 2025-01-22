import networkx as nx 
import random
from UCM import UCM_adjust_opinion
import matplotlib.pyplot as plt 

def opinion_dist(i, j):
    return abs(i - j)

def adjust_opinion(i, j, mu, epsilon, repulsion):
    dist = opinion_dist(i, j)
    if dist < epsilon:
        # Attraction
        i_new = i + mu * (j - i)
        j_new = j + mu * (i - j)
    elif repulsion :
        # Repulsion
        i_new = i - mu * (j - i)
        j_new = j - mu * (i - j)
        
        # ensure i_new and j_new are within [0, 1] in case of extreme repulsion
        i_new = max(0, min(1, i_new))
        j_new = max(0, min(1, j_new))
    else :
        i_new = i
        j_new = j
    return i_new, j_new
    
# TESTING FUNCTIONS 
#def test():
    #i = 0.5
    #j = 0.7
    #print('oldvals: ', i, j)
    #print('newvals: ', adjust_opinion(i, j, 0.25, 0.2, True))
    

def initialize_graph(N):
    '''Creates a Scale-Free graph with N nodes and uniformly random opinions between 0 and 1'''
    g = nx.barabasi_albert_graph(N, 2) # results in a power law between 2 and 3, as per the paper
    opinions = {node: random.uniform(0, 1) for node in g.nodes()} # uniformly random opinions between 0 and 1
    nx.set_node_attributes(g, opinions, 'opinion')
    return g

def run_sim(N, T, mu, epsilon, type, plot=False, progress_bar=False):
    '''
    Runs simulation until T time steps and returns the final graph.
    
    Args:
        N: number of nodes
        T: number of time steps
        mu: parameter for adjusting opinions
        epsilon: threshold for opinion distance
        type: 'RUCM', 'naive_repulsion', or 'RBCM
        plot: whether to plot the final graph
        progress_bar: whether to display a progress bar
    Returns: 
        g: final graph
    '''
    
    assert 0 <= mu <= 1, f"mu out of bounds [0,1]: {mu}"
    assert 0 <= epsilon <= 1, f"epsilon out of bounds [0,1]: {epsilon}"
    
    # Choose the adjustment function based on the type (This is python magic/gore - I'm sorry)
    # This optimizes the code by avoiding if statements in the loop
    if type == 'RUCM':
        adjustment_function = UCM_adjust_opinion
    elif type == 'naive_repulsion':
        adjustment_function = lambda i, j, mu, epsilon: adjust_opinion(i, j, mu, epsilon, True)
    elif type == 'RBCM':
        adjustment_function = lambda i, j, mu, epsilon: adjust_opinion(i, j, mu, epsilon, False)
    else:
        raise ValueError(f"Invalid type: {type}")
    
    g = initialize_graph(N)
    
    for t in range(T):
        # For each node in a random order
        nodes = list(g.nodes())
        random.shuffle(nodes)
        for node in nodes:
            # if node has neighbors (might have been cut off by someone)
            if list(g.neighbors(node)): 
                # pick a random neighbor 
                neighbor = random.choice(list(g.neighbors(node)))
                i = g.nodes[node]['opinion']
                j = g.nodes[neighbor]['opinion']
                
                # adjust opinions (or not, handled by the adjustment function)
                i_new, j_new = adjustment_function(i, j, mu, epsilon)
                g.nodes[node]['opinion'] = i_new
                g.nodes[neighbor]['opinion'] = j_new

                # rewire if opinions are too far apart
                if opinion_dist(i_new, j_new) > epsilon:
                    new_neighbor = random.choice(list(g.nodes()))
                    # ensure new neighbor is not the same as the old one, the node itself, or one of the node's current neighbors
                    while new_neighbor == node or new_neighbor in g.neighbors(node): 
                        new_neighbor = random.choice(list(g.nodes()))
                    g.remove_edge(node, neighbor)
                    g.add_edge(node, new_neighbor)
        
        if progress_bar:
            progress = (t + 1) / T
            bar_length = 60
            block = int(round(bar_length * progress))
            text = f"\rProgress: [{'#' * block + '-' * (bar_length - block)}] {progress * 100:.2f}%"
            print(text, end="")
    
    if plot:
        opinions = nx.get_node_attributes(g, 'opinion')
        pos = nx.spring_layout(g)
    
        fig, ax = plt.subplots(figsize=(8, 8))
    
        # Draw nodes with color based on opinion
        nx.draw_networkx_nodes(g, pos, node_color=list(opinions.values()), cmap=plt.cm.viridis, node_size=10)
        nx.draw_networkx_edges(g, pos, alpha=0.3)
    
        fig.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), ax=ax, label='Opinion')    
        plt.show()
        
    return g

#g = run_sim(2000, 100, epsilon=0.01, mu=0.05, type='RUCM', plot=False, progress_bar=True)

#print(alternate_opinion_distance(0.1, 0.6))

# 2000 nodes
# 10^5 time steps
# 0,0.5 param space 
# 5 repeats
