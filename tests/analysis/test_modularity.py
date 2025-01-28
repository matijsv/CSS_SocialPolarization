import pytest
import networkx as nx
from src.analysis.modularity import (
    count_communities,
    analyze_communities,
    calculate_modularity,
    analyze_modularity
)
from src.core.utils import get_graphs

@pytest.fixture
def simple_graph():
    """Create a simple graph for unit testing."""
    G = nx.erdos_renyi_graph(10, 0.4)  # A random graph with 10 nodes and edge probability 0.4
    return G

def test_count_communities(simple_graph):
    """Test the count_communities function."""
    # Let's test with a simple graph
    communities_count = count_communities(simple_graph)
    assert communities_count >= 1, f"Expected at least one community, got {communities_count}"
    
    # Now, test with a completely disconnected graph (no edges)
    disconnected_graph = nx.Graph()
    disconnected_graph.add_nodes_from(range(5))
    communities_count = count_communities(disconnected_graph)
    assert communities_count == 5, f"Expected 5 communities, got {communities_count}"

def test_calculate_modularity(simple_graph):
    """Test the calculate_modularity function."""
    # Test for modularity of a simple graph
    modularity_value = calculate_modularity(simple_graph)
    assert 0 <= modularity_value <= 1, f"Modularity should be between 0 and 1, got {modularity_value}"

    # Test with a graph that is fully connected, modularity should be higher
    fully_connected_graph = nx.complete_graph(10)
    modularity_value = calculate_modularity(fully_connected_graph)
    assert 0 <= modularity_value <= 1, f"Modularity should be between 0 and 1, got {modularity_value}"

def test_analyze_communities():
    """Test the analyze_communities function."""
    n_runs = 5
    n_nodes = 10
    time_steps = 50
    mu = 0.1
    epsilon_values = [0.1, 0.3, 0.5]  # Range of epsilon values for testing

    # Run the analysis
    avg_communities = analyze_communities(n_runs, n_nodes, time_steps, mu, epsilon_values)
    
    # Ensure the results are returned as expected
    assert len(avg_communities) == len(epsilon_values), "Length of avg_communities doesn't match the number of epsilon values."
    
    for avg_community in avg_communities:
        assert avg_community > 0, f"Expected positive number of communities, got {avg_community}"

def test_analyze_modularity():
    """Test the analyze_modularity function."""
    n_runs = 5
    n_nodes = 10
    time_steps = 50
    mu = 0.1
    epsilon_values = [0.1, 0.3, 0.5]  # Range of epsilon values for testing

    # Run the modularity analysis
    avg_modularities = analyze_modularity(n_runs, n_nodes, time_steps, mu, epsilon_values)
    
    # Ensure the results are returned as expected
    assert len(avg_modularities) == len(epsilon_values), "Length of avg_modularities doesn't match the number of epsilon values."
    
    for avg_modularity in avg_modularities:
        assert 0 <= avg_modularity <= 1, f"Modularity should be between 0 and 1, got {avg_modularity}"

@pytest.mark.parametrize("epsilon,expected", [(0.1, 0.4), (0.5, 0.3), (0.8, 0.5)])
def test_modularity_for_different_epsilon(epsilon, expected):
    """Test that modularity changes correctly with epsilon."""
    n_runs = 1
    n_nodes = 10
    time_steps = 10
    mu = 0.1

    final_graphs, _ = get_graphs(n_runs, n_nodes, time_steps, epsilon, mu)
    
    for graph in final_graphs:
        modularity_value = calculate_modularity(graph)
        assert abs(modularity_value - expected) < 0.1, f"Expected modularity close to {expected} for epsilon={epsilon}, got {modularity_value}"

