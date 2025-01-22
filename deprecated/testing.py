from UCM import UCM_adjust_opinion as new
from UCM_graveyard import UCM_adjust_opinion as old

# Test the function
i = 0.5
j = 0.9
mu = 0.25
epsilon = 0.2
print('new: ', new(i, j, mu, epsilon))
print('old: ', old(i, j, mu, epsilon))