import numpy as np
import scipy.special
from scipy.stats import binom
from scipy.stats import norm

'''
contains functions for calculating the binomial expectations used in results
'''

# calculate the expectation of min(X/l, 1), X ~ Binom(n, p)
def fraction(n, p, l):
    x = np.arange(0, n + 1)
    return np.sum(binom.pmf(x, n, p) * np.minimum(x/l, 1))

# calculate the gaussian approx to the above frac
# quite precise, uses gaussian cdf but not pdf
def fraction_approx(n, p, l):
    q = 1 - p
    t1 = np.sqrt(q / (2 * np.pi * n * p))
    if q > 0 and p > 0:
        F = norm.cdf(l, n * p, np.sqrt(n * p * q))
    else:
        F = float(n * p <= l)
    t2 = F * (1 - ((n * p) / l))
    return 1 - t1 - t2

# proportion of value in the one-round version
# exact: whether exact binomial or gaussian approx is used
def p_one_round(k, c, exact):
    if exact:
        f = fraction
    else:
        f = fraction_approx
    e1 = f(np.floor((1+c) * k), 1 / (1+c), k)
    e2 = f(np.floor((1+c) * k), c / (1+c), np.ceil(c * k))
    e3 = f(k, c, np.ceil(c * k))
    t = c * (e2 + e3 - 1)
    return (k / np.ceil((1 + c) * k)) * (e1 + t) 

# vs: value of the opt ((1+c)k, k) assignment
def one_round_bounds(ks, vs, c, exact):
    bds = []
    for k, v in zip(ks, vs):
        bd = v * p_one_round(k, c, exact)
        bds.append(bd)
    return bds

# proportion of value for the 2 round bound
def p_two_round(k, exact):
    if exact:
        f = fraction
    else:
        f = fraction_approx
    l = np.ceil(k/4) # theory uses ceil(k/4), optimal is floor(k/4)+1
    e1 = f(2*k, 1/8, l)
    e2 = f(k, 1/4, l)
    return e1 + e2 - ((k/4)/l)

# value_21: value of the optimum (2, 1) assignment
# vs_without: value of the (2k, k) assignment without the opt (2, 1)
def two_round_bounds(ks, value_21, vs_without, exact):
    bds = []
    for k, v_without in zip(ks, vs_without):
        p = p_two_round(k, exact)
        bd = (0.75 * value_21) + ((p/4) * v_without)
        bds.append(bd)
    return bds

