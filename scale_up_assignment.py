import numpy as np
from LP import *
from load_sims import *

'''
Gets the value of the optimal (2k, k)-load assignment and saves it.
Used in the one-round assignment lower bound.
'''

fname = 'DA1'
nk = 20

S, M = load_sims('datasets/'+fname)
S, revscale = scale_reviewers(S)
M = np.zeros_like(S)

ks = list(range(1, nk+1))
vs = []
for k in ks:
    v, A = match(S, M, k, k*2)
    num_assignments = k * 2 * S.shape[1]
    avg_val = v / num_assignments
    vs.append(avg_val)
    print(k, avg_val)

np.savez('scale_up_results_' + fname + '.npz', ks=ks, vs=vs, revscale=revscale)
