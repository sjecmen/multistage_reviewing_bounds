import numpy as np
from LP_plus_ideal import *
from load_sims import *

'''
Estimates the expected value of random split with 1 review on each paper in each stage (with reviewer loads scaled up if necessary) and saves data.
'''

fname = 'preflib3'

S, M = load_sims('datasets/' + fname)
revs, paps = S.shape

# for both stages:
papload = 2
revload = 6

second_round_fracs = [0.1, 0.3, 0.5, 1]
results = []

for frac in second_round_fracs:
    num_second_round_paps = int(frac * paps)
    nreviews = (paps + num_second_round_paps) * papload

    num_pap_samples = 10
    results_for_frac = []
    for pap_sample in range(num_pap_samples):
        v, v_opt = split_assignment(S, M, revload, papload, frac) # experimental results
        print(frac, pap_sample, "exp:", v)
        print(frac, pap_sample, "opt:", v_opt)
        
        results_for_frac.append((v, v_opt))
    results.append(results_for_frac)

np.savez('ideal_and_actual_split_'+fname+'.npz', results=results, revload=revload, papload=papload)
