import numpy as np
import scipy.special
from scipy.stats import binom

'''
contains functions for calculating the binomial expectations used in results
'''

# calculate the expectation of min(X/l, 1)
def fraction(num, k, p, l):
    x = np.arange(0, num + 1)
    return np.sum(binom.pmf(x, num, p) * np.minimum(x/l, 1))

# p_{kl} in the (2k, k) bound
def p_one_round(k):
    return fraction(2*k, k, 1/2, k)

# gaussian approximation to p
def approx_one_round(ks):
    return 1 - ( 1 / (2 * np.sqrt(np.asarray(ks) * np.pi)) )

# vs: value of the opt (2k, k) assignment
def one_round_bounds(ks, vs):
    bds = []
    for k, v in zip(ks, vs):
        bd = v * p_one_round(k)
        bds.append(bd)
    return bds

def approx_one_round_bounds(ks, vs):
    ps = approx_one_round(ks)
    bds = ps * np.asarray(vs)
    return bds

# p_{kl} for the 2 round bound
def p_two_round_base(k, l):
    paper_frac = fraction(2*k, k, 1/8, l)
    reviewer_frac = fraction(k, k, 1/4, l)
    return paper_frac + reviewer_frac - (k/(4*l))

# use l=k/4
def p_two_round(k):
    l = np.floor(k/4) + 1#np.ceil(k/4)
    return p_two_round_base(k, l)

# optimize l
def p_two_round_opt(k):
    vs = []
    for l in range(1, k+1):
        v = p_two_round_base(k, l)
        vs.append(v)
    return max(vs)

# gaussian approximation assuming l=k/4
def approx_two_round(ks):
    return 1 - ( (np.sqrt(6) + np.sqrt(7)) / (2 * np.sqrt(np.asarray(ks) * np.pi)) )

# value_21: value of the optimum (2, 1) assignment
# vs_without: value of the (2k, k) assignment without the opt (2, 1)
def two_round_bounds(ks, value_21, vs_without):
    bds = []
    for k, v_without in zip(ks, vs_without):
        p = p_two_round(k)
        bd = (0.75 * value_21) + ((p/4) * v_without)
        bds.append(bd)
    return bds

def approx_two_round_bounds(ks, value_21, vs_without):
    ps = approx_two_round(ks)
    bds = (0.75 * value_21) + ((ps/4) * np.asarray(vs_without))
    return bds


