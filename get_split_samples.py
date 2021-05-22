import numpy as np
from LP import *
from load_sims import *

'''
Runs the main experiment by saving the value of several trials of random split against the optimal
'''

fname = 'query'

S, M = load_sims('datasets/' + fname)
revs, paps = S.shape

# for both stages:
papload = 2
revload = 6
T = 10
cs = [0.1, 0.3, 0.5]
opt_data = {c:[] for c in cs}
split_data = {c:[] for c in cs}


for frac in cs:
    num_second_round_paps = int(frac * paps)
    nreviews = (paps + num_second_round_paps) * papload

    for t in range(T):
        print(frac, t)
        v, v_opt = split_assignment(S, M, revload, papload, frac) # experimental results
        opt_data[frac].append(v_opt/nreviews)
        split_data[frac].append(v/nreviews)

np.savez('split_samples_'+fname+'.npz', opt_samples=opt_data, split_samples=split_data, papload=papload, revload=revload)
