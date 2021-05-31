import numpy as np
from LP import *
from load_sims import *

'''
Estimates the expected value of random split with 1 review on each paper in each stage (with reviewer loads scaled up if necessary) and saves data.
'''

fname = 'query'

S, M = load_sims('datasets/'+fname)
S, revscale = scale_reviewers(S)
M = np.zeros_like(S)

print(S.shape, revscale)
nreviews = 2 * S.shape[1]

samples = []
T = 10
for i in range(T):
    v, _ = split_assignment(S, M, 1, 1, 1, False)
    a = v / nreviews
    print(a)
    samples.append(a)
avg_val = np.mean(a)
print('mean:', avg_val)
np.savez('expected_split_'+fname+'.npz', average_value=avg_val, revload=1, papload=1, samples=samples, revscale=revscale)
