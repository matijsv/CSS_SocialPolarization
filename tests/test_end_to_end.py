import pytest
import numpy as np
from src.core.utils import get_graphs, get_opinion_hist
from src.analysis.isolation import count_disconnected_nodes, analyze_disconnected_nodes

def test_end_to_end_complex_simulation():
    """
    Complex end-to-end test for the simulation pipeline.
    This test ensures the correctness of the simulation results,
    incorporates isolation analysis, and validates the behavior
    with varying epsilon and mu parameters.
    """
    # Test parameters
    n_runs = 2
    n_nodes = 50
    time_steps = 30
    epsilon_values = np.linspace(0.1, 0.5, 3)  # Test 3 epsilon values
    mu_values = np.linspace(0.05, 0.2, 2)  # Test 2 mu values
    test_mu = 0.1
    test_epsilon = 0.3

    # Step 1: Generate graphs for a single epsilon and mu
    final_graphs, initial_graphs = get_graphs(n_runs, n_nodes, time_steps, test_epsilon, test_mu)
    
    # Validate graph integrity
    assert len(final_graphs) == n_runs, "Incorrect number of final graphs"
    assert len(initial_graphs) == n_runs, "Incorrect number of initial graphs"
    for graph in final_graphs + initial_graphs:
        assert len(graph.nodes()) == n_nodes, "Graph does not have the correct number of nodes"
        assert len(graph.edges()) > 0, "Graph is empty or disconnected"

    # Step 2: Analyze disconnected nodes for varying epsilon and mu values
    avg_disconnected_nodes = analyze_disconnected_nodes(
        n_runs=n_runs,
        n_nodes=n_nodes,
        time_steps=time_steps,
        mu=test_mu,
        epsilon_values=epsilon_values,
    )

    # Validate the results of the isolation analysis
    assert len(avg_disconnected_nodes) == len(epsilon_values), "Mismatch in epsilon analysis results"
    for disconnected_count in avg_disconnected_nodes:
        assert disconnected_count >= 0, "Disconnected node count cannot be negative"
        assert disconnected_count <= n_nodes, "Disconnected nodes exceed total node count"

    # Step 3: Simulate and validate opinion histograms
    all_opinions, avg_histogram, avg_isolated = get_opinion_hist(
        n_runs=n_runs,
        n_nodes=n_nodes,
        time_steps=time_steps,
        epsilon=test_epsilon,
        mu=test_mu,
    )

    # Validate histogram and opinions
    assert len(avg_histogram) == 100, "Histogram does not have 100 bins"
    for opinions in all_opinions:
        for opinion in opinions:
            assert 0 <= opinion <= 1, "Opinion out of bounds [0,1]"
    assert avg_isolated >= 0, "Average isolated nodes cannot be negative"
    assert avg_isolated <= n_nodes, "Average isolated nodes exceed total node count"

    # Step 4: Check behavior across epsilon and mu ranges
    for epsilon in epsilon_values:
        for mu in mu_values:
            avg_disconnected_nodes_range = analyze_disconnected_nodes(
                n_runs=n_runs,
                n_nodes=n_nodes,
                time_steps=time_steps,
                mu=mu,
                epsilon_values=[epsilon],
            )
            disconnected_count = avg_disconnected_nodes_range[0]
            assert disconnected_count >= 0, f"Invalid disconnected count for epsilon={epsilon}, mu={mu}"
            assert disconnected_count <= n_nodes, f"Too many disconnected nodes for epsilon={epsilon}, mu={mu}"

    # If all assertions pass, the test is successful
    print("Complex end-to-end simulation test passed.")
