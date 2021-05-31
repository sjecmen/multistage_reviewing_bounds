import numpy as np
import scipy.special
from scipy.stats import binom
from scipy.stats import norm

'''
Contains functions for calculating the binomial expectations used in results
'''

# Calculate the expectation of min(X/l, 1), X ~ Binom(n, p)
def fraction(n, p, l):
    x = np.arange(0, n + 1)
    return np.sum(binom.pmf(x, n, p) * np.minimum(x/l, 1))

# Calculate the gaussian approximation to the above expectation
def fraction_approx(n, p, l):
    q = 1 - p
    t1 = np.sqrt(q / (2 * np.pi * n * p))
    if q > 0 and p > 0:
        F = norm.cdf(l, n * p, np.sqrt(n * p * q))
    else:
        F = float(n * p <= l)
    t2 = F * (1 - ((n * p) / l))
    return 1 - t1 - t2

'''
Constant in the Theorem 6 bound
    k : load of assignment on (R, P)
    c : fraction of papers in stage two
    exact : whether to use exact expectation or approximation
'''
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

'''
Calculate Theorem 6 bounds
    ks : vector, loads of assignments on (R, P)
    vs : vector, values of the opt assignments with l_r = k, l_p = (1+c)k
    c : fraction of papers in stage two
    exact : whether to use exact expectation or approximation
'''
def one_round_bounds(ks, vs, c, exact):
    bds = []
    for k, v in zip(ks, vs):
        bd = v * p_one_round(k, c, exact)
        bds.append(bd)
    return bds

'''
Constant in the Theorem 7 bound
    k : load of assignment on (R, P)
    exact : whether to use exact expectation or approximation
'''
def p_two_round(k, exact):
    if exact:
        f = fraction
    else:
        f = fraction_approx
    l = np.ceil(k/4) # theory uses ceil(k/4), optimal in practice is floor(k/4)+1
    e1 = f(2*k, 1/8, l)
    e2 = f(k, 1/4, l)
    return e1 + e2 - ((k/4)/l)

'''
Calculate Theorem 7 bounds
    ks : vector, loads of assignments on (R, P)
    value_21 : value of the opt assignment with l_r = 1, l_p = 2
    vs_without : vector, values of the opt assignments with l_r = k, l_p = (1+c)k, disjoint from the value_21 assignment
    exact : whether to use exact expectation or approximation
'''
def two_round_bounds(ks, value_21, vs_without, exact):
    bds = []
    for k, v_without in zip(ks, vs_without):
        p = p_two_round(k, exact)
        bd = (0.75 * value_21) + ((p/4) * v_without)
        bds.append(bd)
    return bds

