# SCHEME:
# WORKER RETURNS AN ARRAY INCLUDING 5 RUN-AVERAGED VARIANCE, SIMILARITY, DISCONNECTEDS, NUM COMMUNITIES and MODULARITY
# MAIN, FOR VALUES IN EPSILON COLLECTS ALL THE DATA AND CALCULATES AVERAGES

# SO WORKER NEEDS TO LOOP N-RUNS: 
# RUN SIMULATION (CREATE FINAL GRAPH OBJECT)
# CALL ANALYSIS FUNCTIONS (VARIANCE, SIMILARITY, DISCONNECTEDS, NUM COMMUNITIES, MODULARITY)
# AGREGATE INTO AN ARRAY AND RETURN

# FOR LATER POSSIBLE HEATMAP CREATION LOOK INTO ITERTOOLS.PRODUCT FOR EPSILON AND MU VALUES
# WITH STARMAP

# As stated in the documentation, 
# concurrent.futures.ProcessPoolExecutor is a wrapper around a multiprocessing.Pool.
# As such, the same limitations of multiprocessing apply (e.g. objects need to be pickleable).
# https://stackoverflow.com/questions/38311431/concurrent-futures-processpoolexecutor-vs-multiprocessing-pool-pool

# make num runs a (i think best global) variable

""" def worker_variance_epsilons(epsilon):
    variance = opinions_variance(10, 100, TIME_STEPS, epsilon, DEFAULT_MU)
    return variance

def multiprocess_variance_epsilon(epsilon_values):
    num_workers = min(mp.cpu_count(), len(epsilon_values))
    with mp.Pool(num_workers) as pool:
        list_of_variances = pool.map(worker_variance_epsilons, epsilon_values)

    return list_of_variances

def multiprocess_all_epsilon(epsilon_values):
    
    num_workers = min(mp.cpu_count(), len(epsilon_values))
    with mp.Pool(num_workers) as pool:
        list_of_dicts = pool.map(worker_combined_epsilons, epsilon_values)

    return list_of_dicts

def multiprocess_mod_comm_epsilon(epsilon_values):
    
    num_workers = min(mp.cpu_count(), len(epsilon_values))
    with mp.Pool(num_workers) as pool:
        list_of_dicts = pool.map(worker_mod_comm_epsilons, epsilon_values)

    return list_of_dicts

def multiprocess_mod_comm_both(epsilon_values, mu_values):
    param_grid = list(itertools.product(epsilon_values, mu_values))
    num_workers = min(mp.cpu_count(), len(param_grid))
    with mp.Pool(num_workers) as pool:
        list_of_dicts = pool.starmap(worker_mod_comm_both, param_grid)

    return list_of_dicts

def worker_combined_epsilons(epsilon):
    results_dict = combined_analysis(N_RUNS, N_NODES, TIME_STEPS, epsilon, DEFAULT_MU)
    results_dict['epsilon'] = epsilon
    return results_dict

def worker_mod_comm_epsilons(epsilon):
    results_dict = modules_communities_analysis(N_RUNS, N_NODES, TIME_STEPS, epsilon, DEFAULT_MU)
    results_dict['epsilon'] = epsilon
    return results_dict

def worker_mod_comm_both(epsilon, mu):
    results_dict = modules_communities_analysis(N_RUNS, N_NODES, TIME_STEPS, epsilon, mu)
    results_dict['epsilon'] = epsilon
    results_dict['mu'] = mu
    return results_dict """