def rho(x):
    '''Function used to guarantee periodic boundary conditions as per eq 1 in paper'''
    assert -1 <= x <= 1, f"x is out of bounds [-1, 1]: {x}"
    if -1 <= x <= -0.5:
        return -1
    if -0.5 < x < 0.5:
        return 0
    if 0.5 <= x <= 1:
        return 1

def UCM_adjust_opinion(i, j, mu, epsilon):
    '''Adjusts opinions i and j based on the given parameters as per eq 2 & 3 in paper '''
    
    assert 0 <= i <= 1, f"Opinion i is out of bounds: {i}"
    assert 0 <= j <= 1, f"Opinion j is out of bounds: {j}"
    
    i_min_j = i - j
    alt_dist = i_min_j- rho(i - j)
    abs_alt_dist = abs(alt_dist)
    j_min_i = j - i
    
    if abs_alt_dist < epsilon: 
        i_new = i + mu * j_min_i
        j_new = j + mu * i_min_j
        
    if abs_alt_dist >= epsilon:
        i_new = i - mu * (j_min_i - rho(j - i))
        j_new = j - mu * alt_dist
        
        # ensure i_new and j_new are within [0, 1] in case of extreme repulsion
        i_new = max(0, min(1, i_new))
        j_new = max(0, min(1, j_new))
        
    return i_new, j_new

