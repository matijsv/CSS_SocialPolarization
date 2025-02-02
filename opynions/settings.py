''' The constants used when creating results shown in the presentation'''

import numpy as np 

EPSILON_VALUES = np.linspace(0,0.5,51)
MU_VALUES = np.linspace(0,0.5,51)
N_RUNS = 5 # Runs to be averaged over
TIME_STEPS = 100 # The amount of timesteps to iterate the network over
N_NODES = 2000 # The size of the networks.
M_BA = 2 # Parameter for the barabasi albert graph generator DEFAULT = 2

