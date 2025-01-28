import pytest
import networkx as nx
import numpy as np
from unittest.mock import patch
from src.analysis.combined import combined_analysis
from src.core.utils import get_graphs
from src.analysis.similarity import compute_neighbor_similarity

@pytest.fixture
def mock_graphs():
    """
    Fixture to simulate graphs with opinion attributes and varying structures.
    """
    # Create a list of mock graphs
    graphs = []
    for _ in range(3):  # Simulating 3 runs
        G = nx.Graph()
        # Add nodes with 'opinion' attributes
        for j in range(10):
            G.add_node(j, opinion=np.random.uniform(0, 1))
        # Add edges to create some connections
        edges = [(j, (j + 1) % 10) for j in range(10)]
        G.add_edges_from(edges)
        graphs.append(G)
    return graphs

@pytest.mark.parametrize(
    "n_runs, n_nodes, time_steps, epsilon, mu, expected",
    [
        (
            3, 10, 5, 0.1, 0.2, 
            {
                "variance": 0.08, 
                "avg_isolated": 0.0, 
                "avg_num_communities": 1.0, 
                "avg_modularity": 0.5, 
                "avg_similarity": 0.9
            },
        )
    ],
)
def test_combined_analysis(mock_graphs, n_runs, n_nodes, time_steps, epsilon, mu, expected):
    """
    Test combined analysis function with mocked graphs and predefined expected results.
    """
    with patch("src.core.utils.get_graphs", return_value=(mock_graphs, None)), \
         patch("src.analysis.similarity.compute_neighbor_similarity", return_value=0.9):
        
        # Run the combined analysis
        results = combined_analysis(n_runs, n_nodes, time_steps, epsilon, mu)

        # Validate results against expected values
        for key, expected_value in expected.items():
            assert abs(results[key] - expected_value) < 0.1, f"Expected {key} to be close to {expected_value}, but got {results[key]}"
