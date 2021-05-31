import numpy as np
from LP import *
from load_sims import *

'''
Gets the value of the (k, 2k)-load assignment after removing the optimal (1, 2)-load assignment.
Used in the Theorem 7 bound.
'''

fname = 'iclr2018'
nk = 20

S, M = load_sims('datasets/'+fname)
S, revscale = scale_reviewers(S)
M = np.zeros_like(S)

v21, A = match(S, M, 1, 2)
for i in range(S.shape[0]):
    for j in range(S.shape[1]):
        if A[i][j] == 1:
            M[i, j] = 1
v21 /= (2 * S.shape[1])
print('2, 1 value', v21)

ks = list(range(1, nk+1))
vs = []
for k in ks:
    v, A = match(S, M, k, k*2)
    num_assignments = k * 2 * S.shape[1]
    avg_val = v / num_assignments
    vs.append(avg_val)
    print(k, avg_val)

np.savez('scale_up_results_without_21_' + fname + '.npz', ks=ks, vs=vs, revscale=revscale, v21=v21)
