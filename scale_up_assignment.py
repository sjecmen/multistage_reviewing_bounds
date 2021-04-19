import numpy as np
from LP import *
from load_sims import *

'''
Gets the value of the optimal (2k, k) assignment and saves it.
'''

fname = 'iclr2018'
nk = 100

S, M = load_sims(fname)

nreviews = 2 * S.shape[1]
revload_scale = int(np.ceil(nreviews / S.shape[0]))

ks = list(range(1, nk+1))
vs = []
for k in ks:
    v, A = match(S, M, k*revload_scale, k*2)
    num_assignments = k * 2 * S.shape[1]
    avg_val = v / num_assignments
    vs.append(avg_val)
    print(k, avg_val)

np.savez('scale_up_results_' + fname + '.npz', ks=ks, vs=vs, revload_scale=revload_scale)
