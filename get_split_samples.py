import numpy as np
from LP import *
from load_sims import *

'''
Samples several random stage-two paper sets, and calculates value of a sample of random reviewer split and the ex-post optimum value for each.
    papersplit indicates whether we are in the paper-split model (papers only in one stage).
'''

fname = 'iclr2018'
papersplit = False
print(fname, papersplit)

S, M = load_sims('datasets/' + fname)
revs, paps = S.shape

# for both stages:
if not papersplit:
    papload = 2
    revload = 6
    if fname == 'preflib2':
        revload = 12
    if fname == 'DA2':
        revload = 12
    cs = [0.1, 0.3, 0.5]
    num_second_round_paps = int(frac * paps)
    nreviews = (paps + num_second_round_paps) * papload
else:
    papload = 3
    revload = 6
    cs = [0.5]
    nreviews = paps * papload
T = 10
opt_data = {c:[] for c in cs}
split_data = {c:[] for c in cs}


for frac in cs:
    for t in range(T):
        print(frac, t)
        v, v_opt = split_assignment(S, M, revload, papload, frac, True, papersplit)
        opt_data[frac].append(v_opt/nreviews)
        split_data[frac].append(v/nreviews)

if papersplit:
    js = '_papersplit'
else:
    js = ''
np.savez('split_samples_'+fname+js+'.npz', opt_samples=opt_data, split_samples=split_data, papload=papload, revload=revload)
