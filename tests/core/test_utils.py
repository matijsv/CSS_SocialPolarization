import pytest
import networkx as nx
from src.core.utils import get_graphs

def test_get_graphs():
    n_runs = 3
    n_nodes = 10
    time_steps = 5
    epsilon = 0.2
    mu = 0.1

    # Step 1: Generate graphs using `get_graphs`
    final_graphs, initial_graphs = get_graphs(n_runs, n_nodes, time_steps, epsilon, mu)
    
    # Ensure the correct number of graphs are returned
    assert len(final_graphs) == n_runs, "Incorrect number of final graphs"
    assert len(initial_graphs) == n_runs, "Incorrect number of initial graphs"

    # Ensure the graphs are non-empty and contain the correct number of nodes
    for graph in final_graphs + initial_graphs:
        assert len(graph.nodes()) == n_nodes, "Graph does not have the correct number of nodes"
        assert len(graph.edges()) > 0, "Graph is empty or disconnected"

