import numpy as np

# Set the parameters
N_runs = 5
N_nodes = 2000
time_steps = 100
mu = 0.25
epsilon_values =  np.linspace(0.0, 0.5, num=5)
# num_communities = analysis.analyze_communities(N_runs, N_nodes, time_steps, mu, epsilon_values)

#plot_communities(epsilon_values, num_communities)

""" #usage
if __name__ == "__main__":
    # Parameters
    N_RUNS = 5           # Number of simulations per parameter combination
    N_NODES = 2000       # Number of nodes in each graph
    TIME_STEPS = 100     # Number of time steps
    EPSILON_RANGE = (0, 0.5, 51)  # Epsilon values from 0 to 0.5 (51 steps)
    MU_RANGE = (0, 0.5, 51)       # Mu values from 0 to 0.5 (51 steps)
    OUTPUT_FILE = "disconnected_nodes_matrix.csv"

    # Generate the matrix and save to file
    generate_disconnected_nodes_matrix(N_RUNS, N_NODES, TIME_STEPS, EPSILON_RANGE, MU_RANGE, OUTPUT_FILE)

 """
 

""" # usage
if __name__ == "__main__":
    # Parameters
    N_RUNS = 5           # Number of simulations per parameter combination
    N_NODES = 2000       # Number of nodes in each graph
    TIME_STEPS = 100     # Number of time steps
    EPSILON_RANGE = (0, 0.5, 51)  # Epsilon values from 0 to 0.5 (51 steps)
    MU_RANGE = (0, 0.5, 51)       # Mu values from 0 to 0.5 (51 steps)
    OUTPUT_FILE = "modularity_matrix.csv"

    # Generate the matrix and save to file
    generate_modularity_matrix(N_RUNS, N_NODES, TIME_STEPS, EPSILON_RANGE, MU_RANGE, OUTPUT_FILE) """
    

""" 
if __name__ == "__main__":
    # Parameters
    N_RUNS = 5           # Number of simulations per epsilon value
    N_NODES = 2000       # Number of nodes in each graph
    TIME_STEPS = 100     # Number of time steps
    MU = 0.25            # Adjustment parameter
    EPSILON_VALUES = np.linspace(0, 1, 20)  # Range of epsilon values (0 to 1 in 20 steps)

    # Analyze disconnected nodes for varying epsilon values
    disconnected_nodes = analyze_disconnected_nodes(N_RUNS, N_NODES, TIME_STEPS, MU, EPSILON_VALUES)

    # Plot the results
    plot_disconnected_nodes(EPSILON_VALUES, disconnected_nodes)

 """
 
""" if __name__ == "__main__":
    # Parameters
    N_RUNS = 5               # Number of runs per parameter combination
    N_NODES = 2000           # Number of nodes in each graph
    TIME_STEPS = 100         # Number of time steps per simulation
    MU_VALUES = np.linspace(0, 0.5, 51)       # 51 values for mu (0 to 0.5)
    EPSILON_VALUES = np.linspace(0, 0.5, 51)  # 51 values for epsilon (0 to 0.5)
    OUTPUT_FILE = "neighbor_opinion_similarity_matrix.csv"

    # Run the experiment
    opinion_matrix_experiment(N_RUNS, N_NODES, TIME_STEPS, MU_VALUES, EPSILON_VALUES, OUTPUT_FILE)
 """