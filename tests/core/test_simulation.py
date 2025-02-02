import pytest
import networkx as nx
from opynions.core.simulation import rho, UCM_adjust_opinion, initialize_graph, run_sim

# Test cases for rho
@pytest.mark.parametrize("x, expected", [
    (-1, -1),
    (-0.6, -1),
    (-0.5, 0),
    (0, 0),
    (0.5, 0),
    (0.6, 1),
    (1, 1)
])
def test_rho(x, expected):
    assert rho(x) == expected

@pytest.mark.parametrize("x", [-1.5, 1.5, 2, -2])
def test_rho_invalid_input(x):
    with pytest.raises(AssertionError):
        rho(x)

# Test cases for UCM_adjust_opinion
@pytest.mark.parametrize("i, j, mu, epsilon, expected", [
    (0.2, 0.3, 0.1, 0.5, (0.21, 0.29)),  # Within epsilon, opinions adjust
    (0.9, 0.1, 0.2, 0.5, (0.74, 0.26)),  # Outside epsilon, repulsion
    (0.5, 0.5, 0.3, 0.1, (0.5, 0.5)),    # Opinions stay the same
])
def test_UCM_adjust_opinion(i, j, mu, epsilon, expected):
    i_new, j_new = UCM_adjust_opinion(i, j, mu, epsilon)
    assert round(i_new, 2) == round(expected[0], 2)
    assert round(j_new, 2) == round(expected[1], 2)

@pytest.mark.parametrize("i, j, mu, epsilon", [
    (-0.1, 0.5, 0.1, 0.5),  # Invalid opinion i
    (0.5, 1.1, 0.1, 0.5),   # Invalid opinion j
    #(0.5, 0.5, 1.1, 0.5),   # Invalid mu
    #(0.5, 0.5, 0.5, 1.1),   # Invalid epsilon
])
def test_UCM_adjust_opinion_invalid_input(i, j, mu, epsilon):
    with pytest.raises(AssertionError):
        UCM_adjust_opinion(i, j, mu, epsilon)

# Test cases for initialize_graph
def test_initialize_graph():
    N = 10
    graph = initialize_graph(N)

    # Check graph properties
    assert len(graph.nodes) == N
    assert nx.is_connected(graph)  # Barabási-Albert graphs are connected

    # Check if opinions are set as node attributes
    for node, data in graph.nodes(data=True):
        assert 'opinion' in data
        assert 0 <= data['opinion'] <= 1  # Opinions should be within [0, 1]

"""
@pytest.mark.parametrize("N", [0, -1, 1.5])
def test_initialize_graph_invalid_input(N):
    #with pytest.raises(ValueError):
        initialize_graph(N)

        """
# Test cases for run_sim
def test_run_sim():
    N = 10
    T = 5
    mu = 0.1
    epsilon = 0.2

    g_final, g_init = run_sim(N, T, mu, epsilon)

    # Verify the graphs
    assert len(g_final.nodes) == N
    assert len(g_init.nodes) == N

    # Check if opinions in the final graph are still in [0, 1]
    for node, data in g_final.nodes(data=True):
        assert 'opinion' in data
        assert 0 <= data['opinion'] <= 1

@pytest.mark.parametrize("N, T, mu, epsilon", [
    (-10, 5, 0.1, 0.2),  # Invalid N
    (10, -5, 0.1, 0.2),  # Invalid T
    (10, 5, -0.1, 0.2),  # Invalid mu
    (10, 5, 0.1, -0.2),  # Invalid epsilon
])
def test_run_sim_invalid_input(N, T, mu, epsilon):
    with pytest.raises(AssertionError):
        run_sim(N, T, mu, epsilon)
