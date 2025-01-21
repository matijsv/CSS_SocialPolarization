import networkx as nx 
import random
from UCM_graveyard import UCM_adjust_opinion
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
    

def initialize_graph():
    g = nx.barabasi_albert_graph(2000, 5)
    random.seed(42)
    opinions = {node: random.uniform(0, 1) for node in g.nodes()}
    nx.set_node_attributes(g, opinions, 'opinion')
    return g

def run_sim(N, T, mu, epsilon, type):
    '''
    N: number of nodes
    T: number of time steps
    mu: parameter for adjusting opinions
    epsilon: threshold for opinion distance
    type: 'RUCM', 'naive_repulsion', or 'RBCM
    '''
    g = initialize_graph()

    for t in range(T):
        for node in g.nodes(): # for each node
            if list(g.neighbors(node)): # if node has neighbors (might have been cut off by someone)
                neighbor = random.choice(list(g.neighbors(node)))
                i = g.nodes[node]['opinion']
                j = g.nodes[neighbor]['opinion']
                
                if type == 'RUCM':
                    i_new, j_new = UCM_adjust_opinion(i, j, mu, epsilon)
                elif type == 'naive_repulsion':
                    i_new, j_new = adjust_opinion(i, j, mu, epsilon, repulsion=True)
                elif type == 'RBCM':
                    i_new, j_new = adjust_opinion(i, j, mu, epsilon, repulsion=False)
                else:
                    raise ValueError(f"Invalid type: {type}")
                
                g.nodes[node]['opinion'] = i_new
                g.nodes[neighbor]['opinion'] = j_new

                if opinion_dist(i_new, j_new) > epsilon:
                    g.remove_edge(node, neighbor)
                    new_neighbor = random.choice(list(g.nodes()))
                    # ensure new neighbor is not the same as the old one or the node itself
                    while new_neighbor == neighbor or new_neighbor == node: 
                        new_neighbor = random.choice(list(g.nodes()))
                    g.add_edge(node, new_neighbor)
                
    opinions = nx.get_node_attributes(g, 'opinion')
    pos = nx.spring_layout(g)
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Draw nodes with color based on opinion
    nx.draw_networkx_nodes(g, pos, node_color=list(opinions.values()), cmap=plt.cm.viridis, node_size=10)
    nx.draw_networkx_edges(g, pos, alpha=0.3)
    
    fig.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), ax=ax, label='Opinion')
    plt.show()

run_sim(2000, 100, epsilon=0.1, mu=0.05, type='RUCM')


#print(alternate_opinion_distance(0.1, 0.6))

# 2000 nodes
# 10^5 time steps
# 0,0.5 param space 
# 5 repeats


    