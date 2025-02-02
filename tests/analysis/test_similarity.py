import pytest
import networkx as nx
import numpy as np
import pandas as pd
from src.analysis.similarity import (
    compute_neighbor_similarity,
    analyze_neighbor_similarity,
    opinion_matrix_experiment
)
from src.core.utils import get_graphs


@pytest.fixture
def simple_graph():
    """Fixture to create a simple graph with opinions for testing."""
    G = nx.Graph()
    # Add nodes with opinions as node attributes
    G.add_node(1, opinion=0.5)
    G.add_node(2, opinion=0.8)
    G.add_node(3, opinion=0.2)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    return G


def test_compute_neighbor_similarity(simple_graph):
    """Test the compute_neighbor_similarity function."""
    similarity = compute_neighbor_similarity(simple_graph)
    assert 0 <= similarity <= 1, f"Similarity should be between 0 and 1, got {similarity}"

    # Edge case: graph with no edges
    no_edges_graph = nx.Graph()
    no_edges_graph.add_nodes_from([1, 2, 3])
    similarity = compute_neighbor_similarity(no_edges_graph)
    assert similarity == 0, f"Expected similarity to be 0 for a graph with no edges, got {similarity}"

    # Edge case: graph with all nodes having the same opinion
    same_opinion_graph = nx.Graph()
    same_opinion_graph.add_nodes_from([1, 2, 3])
    same_opinion_graph.add_edge(1, 2)
    same_opinion_graph.add_edge(2, 3)
    for node in same_opinion_graph.nodes():
        same_opinion_graph.nodes[node]['opinion'] = 0.5
    similarity = compute_neighbor_similarity(same_opinion_graph)
    assert similarity == 1.0, f"Expected similarity to be 1.0 for a graph with the same opinions, got {similarity}"


def test_analyze_neighbor_similarity():
    """Test the analyze_neighbor_similarity function."""
    n_runs = 5
    n_nodes = 10
    time_steps = 50
    mu = 0.1
    epsilon_values = [0.1, 0.3, 0.5]  # Range of epsilon values for testing

    # Run the analysis
    avg_similarities = analyze_neighbor_similarity(n_runs, n_nodes, time_steps, mu, epsilon_values)
    
    # Ensure the results are returned as expected
    assert len(avg_similarities) == len(epsilon_values), "Length of avg_similarities doesn't match the number of epsilon values."
    
    for avg_similarity in avg_similarities:
        assert 0 <= avg_similarity <= 1, f"Similarity should be between 0 and 1, got {avg_similarity}"


def test_opinion_matrix_experiment(tmp_path):
    """Test the opinion_matrix_experiment function and ensure it saves a CSV file."""
    n_runs = 3
    n_nodes = 10
    time_steps = 50
    mu_values = [0.1, 0.3, 0.5]
    epsilon_values = [0.1, 0.3, 0.5]
    
    output_file = tmp_path / "opinion_matrix.csv"
    
    # Run the experiment
    opinion_matrix_experiment(n_runs, n_nodes, time_steps, mu_values, epsilon_values, str(output_file))
    
    # Ensure the file was created
    assert output_file.exists(), f"Expected CSV file at {output_file}, but it does not exist."
    
    # Load the CSV file to ensure it's not empty
    df = pd.read_csv(output_file, index_col=0)
    assert not df.empty, "The resulting CSV file is empty."
    
    # Ensure the dimensions of the DataFrame match the expected matrix size
    assert df.shape == (len(mu_values), len(epsilon_values)), "Matrix dimensions do not match the expected size."

    # Optionally, check if the values in the CSV are within a valid range
    for value in df.values.flatten():
        assert 0 <= value <= 1, f"Similarity value should be between 0 and 1, but found {value}"
