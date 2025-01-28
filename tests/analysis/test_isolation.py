import pytest
import networkx as nx
from src.analysis.isolation import count_disconnected_nodes, analyze_disconnected_nodes

# Test for count_disconnected_nodes
def test_count_disconnected_nodes():
    # Create a graph with 3 disconnected nodes and 2 connected nodes
    graph = nx.Graph()
    graph.add_nodes_from([1, 2, 3, 4, 5])
    graph.add_edges_from([(4, 5)])
    
    # Expecting 3 disconnected nodes
    assert count_disconnected_nodes(graph) == 3

def mock_get_graphs(n_runs, n_nodes, time_steps, epsilon, mu):
    # Mock implementation of get_graphs to return disconnected and connected graphs
    graphs = []
    for _ in range(n_runs):
        graph = nx.Graph()
        graph.add_nodes_from(range(n_nodes))
        if epsilon < 0.5:
            # Add edges for connected nodes if epsilon < 0.5
            for i in range(n_nodes - 1):
                graph.add_edge(i, i + 1)
        graphs.append(graph)
    return graphs, None

# Test for analyze_disconnected_nodes
def test_analyze_disconnected_nodes(monkeypatch):
    # Mock the get_graphs function
    monkeypatch.setattr("src.analysis.isolation.get_graphs", mock_get_graphs)

    n_runs = 2
    n_nodes = 5
    time_steps = 10
    mu = 0.1
    epsilon_values = [0.1, 0.6]

    # For epsilon = 0.1, expect 0 disconnected nodes; for epsilon = 0.6, expect 5
    result = analyze_disconnected_nodes(n_runs, n_nodes, time_steps, mu, epsilon_values)
    assert result == [0, 5]
