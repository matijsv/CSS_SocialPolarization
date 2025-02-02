import numpy as np
import matplotlib.pyplot as plt
from src.analysis.multiprocessing import multiprocess_variance_epsilon
from src.core.utils import get_opinion_hist
import src.core.simulation

M_list = np.linspace(1,50,2)
epsilon_values = np.linspace(0.01,0.48,30)
list_of_lists = []
for M in M_list:
    src.core.simulation.M_GRAPH = M
    list_of_variances = multiprocess_variance_epsilon(epsilon_values)
    list_of_lists.append(list_of_variances)

for i, list in enumerate(list_of_lists):
    plt.plot(epsilon_values, list_of_variances, label=f'M: {M_list[i]}')
    
plt.xlabel('Epsilon values')
plt.ylabel('Variance')
plt.title('Variance vs Epsilon values for different node sizes')
plt.legend()
plt.show() 
""" 
epsilon_values = np.linspace(0.01,0.48,20)
variances = []
for eps in epsilon_values:
    all_opinions, _, _ = get_opinion_hist(100,15,100,eps,0.3)
    flattened_opinions = [opinion for run in all_opinions for opinion in run]
    var = np.var(flattened_opinions)
    variances.append(var)

plt.plot(variances,epsilon_values)
plt.xlabel('Epsilon values')
plt.ylabel('Variance')
plt.title('Variance vs Epsilon values for different node sizes')
plt.legend()
plt.show() """