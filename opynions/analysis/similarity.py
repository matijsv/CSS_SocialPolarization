'''Functions for analyzing the similarity of opinions between neighbors in a graph.'''

from opynions.core.utils import get_graphs

def compute_neighbor_similarity(graph):
    """
    Computes the average similarity of opinions between neighbors in the graph.

    Args:
        graph (networkx.Graph): The graph with 'opinion' as a node attribute.

    Returns:
        float: Average similarity of opinions between neighbors.
    """
    total_similarity = 0
    total_edges = 0

    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            opinion_node = graph.nodes[node]['opinion']
            opinion_neighbor = graph.nodes[neighbor]['opinion']
            total_similarity += 1 - abs(opinion_node - opinion_neighbor) # Similarity = 1 - distance
            total_edges += 1

    if total_edges == 0:  # Avoid division by zero
        return 0

    return total_similarity / total_edges

def analyze_neighbor_similarity(n_runs, n_nodes, time_steps, mu, epsilon_values):
    """
    Analyzes and calculates the average neighbor similarity for a range of epsilon values.

    Args:
        n_runs (int): Number of runs for each epsilon value.
        n_nodes (int): Number of nodes in the graph.
        time_steps (int): Number of time steps in the simulation.
        mu (float): Parameter for adjusting opinions.
        epsilon_values (list or numpy.ndarray): Range of epsilon values to test.

    Returns:
        list: Average neighbor similarity values for each epsilon value.
    """
    avg_similarities = []

    for epsilon in epsilon_values:
        print(f"Analyzing neighbor similarity for epsilon = {epsilon:.3f}")
        total_similarity = 0

        # Generate graphs for the given epsilon
        final_graphs, _ = get_graphs(n_runs, n_nodes, time_steps, epsilon, mu)

        # Calculate neighbor similarity for each graph and accumulate the total
        for graph in final_graphs:
            total_similarity += compute_neighbor_similarity(graph)

        # Compute the average similarity for this epsilon
        avg_similarity = total_similarity / n_runs
        avg_similarities.append(avg_similarity)

    return avg_similarities