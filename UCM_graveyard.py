

def rho(x):
    '''Function used to guarantee periodic boundary conditions as per eq 1 in paper'''
    
    assert -1 <= x <= 1, f"x is out of bounds [-1, 1]: {x}"
    if -1 <= x <= -0.5:
        return -1
    if -0.5 < x < 0.5:
        return 0
    if 0.5 <= x <= 1:
        return 1
    
def alternate_opinion_distance(i, j):
    '''Alternate Opinion distance as per first eq under methods in paper (not labelled)'''
    return abs(i - j - rho(i - j)) # note that this is not abs val like in the paper, for optimization purposes

def UCM_adjust_opinion(i, j, mu, epsilon):
    '''Adjusts opinions i and j based on the given parameters as per eq 2 & 3 in paper '''
    
    assert 0 <= i <= 1, f"Opinion i is out of bounds: {i}"
    assert 0 <= j <= 1, f"Opinion j is out of bounds: {j}"
    
    alt_dist = alternate_opinion_distance(i, j)
    if alt_dist < epsilon: 
        i_new = i + mu * (j - i)
        j_new = j + mu * (i - j)
        
    if alt_dist >= epsilon:
        i_new = i - mu * (j - i - rho(j - i))
        j_new = j - mu * (i - j - rho(i - j))
        
        # ensure i_new and j_new are within [0, 1] in case of extreme repulsion
        i_new = max(0, min(1, i_new))
        j_new = max(0, min(1, j_new))
        
    return i_new, j_new