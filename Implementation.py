import numpy as np
import pandas as pd
import networkx as nx
import pickle
import matplotlib.pyplot as plt

def network(n, m, save_excel = False):
    """
    Function to generate free-scale network with initial opinions uniformly distributed on [0,1]. 
    If save_excel specified as True, the function saves the Network to an Excel file.

    Parameters:
        n (int) : Number of nodes.
        m (int): Number of edges to attach from one node to other nodes when generating the network. 
        save_excel: If True the network is saved to an Excel file.  

    Returns: 
        Network with specified parameters    
    """
    network = nx.barabasi_albert_graph(n, m, seed=103)
    opinions = np.random.uniform(0,1,n)

    for i in range(n):
        network.nodes[i]["opinion"] = opinions[i]

    # Save with gpickle
    #nx.write_gpickle(network, "f{network_name}.gpickle")
    #print("Graph saved")    

    #Save to Excel
    if save_excel == True:
        # Edge data
        node_data = [(i, network.nodes[i]['opinion']) for i in network.nodes()]
        node_df = pd.DataFrame(node_data, columns=["Node", "Opinion"])
        
        # Edge data
        edge_data = [(u, v) for u, v in network.edges()]
        edge_df = pd.DataFrame(edge_data, columns=["Source", "Target"])
        
        # Write to Excel
        with pd.ExcelWriter("Network.xlsx") as writer:
            node_df.to_excel(writer, sheet_name="Nodes", index=False)
            edge_df.to_excel(writer, sheet_name="Edges", index=False)
        
        print("Network data saved to 'Network.xlsx'")
    
    return network

def rho(input):
    """
    Rho function as defined in the paper. 

    Parameters: 
        input (float) : usually given as a difference between two opinions. 

    Returns: 
        - -1 if input is in a rage [-1,-0.5)
        - 0 if input is in a range [-0.5,0.5]
        - 1 if input is in a range (0.5,1]
    """
    if input >= -1 and input < -0.5:
        rho = -1
    elif input >= -0.5 and input <= 0.5:
        rho = 0 
    elif input > 0.5 and input <= 1:
        rho = 1
    else:
        raise ValueError(f"Input {input} is out of the expected range [-1, 1].")
    return rho

def tau_measure(opinion1, opinion2):
    """
    Function measuring the distance between two opinions. 

    Parameters:
        opinion1 (float) : Number in the range [0,1], indicates the opinion of node i.
        opinion2 (float) : Number in the range [0,1], indicates the opinion of node j.

    Returns:
        tau_measure between opinions as defined in the paper.

    """
    return abs(opinion1 - opinion2 - rho(opinion1 - opinion2))

def concordant(opinion1, opinion2, miu):
    """
    Function returns adjusted opinions when two concordant opinions interact.

    Parameters:
        opinion1 (float) : Number in the range [0,1], indicates the opinion of node i.
        opinion2 (float) : Number in the range [0,1], indicates the opinion of node j.
        miu (float) : Number in the range [0,0.5], convergence parameter. 

    Returns:
        - updated_opinion1 - updated opinion of node i
        - updated_opinion2 - updated opinion of node j. 

    """
    updated_opinion1 = opinion1 + miu*(opinion2 - opinion1)
    updated_opinion2 = opinion2 + miu*(opinion1 - opinion2)
    return updated_opinion1, updated_opinion2

def discordant(opinion1, opinion2, miu):
    """
    Function returns adjusted opinions when two discordant opinions interact.

    Parameters:
        opinion1 (float) : Number in the range [0,1], indicates the opinion of node i.
        opinion2 (float) : Number in the range [0,1], indicates the opinion of node j.
        miu (float) : Number in the range [0,0.5], convergence parameter.

    Returns:
        - updated_opinion1 - updated opinion of node i
        - updated_opinion2 - updated opinion of node j. 

    """ 
    updated_opinion1 = opinion1 - miu*(rho(opinion2 - opinion1))
    updated_opinion2 = opinion2 - miu*(rho(opinion1 - opinion2))
    return updated_opinion1, updated_opinion2

