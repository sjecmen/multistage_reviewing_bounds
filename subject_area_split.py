import numpy as np
from scipy.stats import sem
from LP import *

rng = np.random.default_rng()

'''
Generate a similarity matrix with subject areas.
Each reviewer and paper one random subject area and a prob of having each other area
Each area match gives you 1 similarity, scaled down by the max similarity
'''
def generate_subject_area(nrev, npap, num_areas, prob):
    def gen(n, a, p):
        X = np.zeros((n, a))
        extras = rng.random((n, a))
        X[extras < p] = 1
        base = rng.choice(a, n)
        for i in range(n):
            X[i, base[i]] = 1
        return X

    R = gen(nrev, num_areas, prob)
    P = gen(npap, num_areas, prob)
    S = (R @ P.T)
    S /= num_areas#np.max(S)
    return S


cs = [0.5]#[0.1, 0.3, 0.5, 1]
ns = list(range(20, 101, 5))
papload = 2
revload = 6
num_areas = 10
p = 0.25
T = 100

opt_data = {c:[] for c in cs}
split_data = {c:[] for c in cs}
for c in cs:
    for n in ns:
        print(c, n)
        num_reviews = (n + int(c*n)) * papload
        opt_avgs = np.zeros(T)
        split_avgs = np.zeros(T)
        for t in range(T):
            S = generate_subject_area(n, n, num_areas, p)
            split_val, opt_val = split_assignment(S, np.zeros_like(S), revload, papload, c)

            opt_avg = opt_val / num_reviews
            opt_avgs[t] = opt_avg

            split_avg = split_val / num_reviews
            split_avgs[t] = split_avg
        print(np.mean(opt_avgs), np.mean(split_avgs))
        opt_data[c].append((np.mean(opt_avgs), sem(opt_avgs)))
        split_data[c].append((np.mean(split_avgs), sem(split_avgs)))
    np.savez('subject_area_data_2.npz', opt_data=opt_data, split_data=split_data, papload=papload, revload=revload, num_trials=T, num_areas=num_areas, ns=ns)
