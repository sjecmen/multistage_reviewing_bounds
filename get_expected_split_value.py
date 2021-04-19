import numpy as np
from LP import *
from load_sims import *

'''
Estimates the expected value of random split with 1 review on each paper in each stage (with reviewer loads scaled up if necessary) and saves data.
'''

fname = 'iclr2018'

S, M = load_sims(fname)
papload = 1
nreviews = 2 * S.shape[1] * papload
revload = int(np.ceil(nreviews / S.shape[0]))

T = 10
t = 0
for i in range(T):
    v, _ = split_assignment(S, M, revload, papload)
    print(v)
    t += v
t /= T
a = t / nreviews
print(a)
np.savez('expected_split_'+fname+'.npz', total_value=t, average_value=a, revload=revload, papload=papload)
