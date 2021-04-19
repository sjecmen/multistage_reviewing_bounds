import numpy as np
from load_sims import *
import matplotlib.pyplot as plt
from bounds import *

''' 
Plots bounds for both the 2 round and 1 round in-expectation bounds. Uses input from the scale_up_assignment, scale_up_assignment_without_21, and get_expected_split_value files if available. 
'''

fname = 'DA1'

if fname == 'all_ones':
    nk = 1000
    n = 1000
    vs = [1 for k in range(1, nk+1)]
    vs_without = [1 for k in range(1, nk+1)]
    rand_value = 1
    value_21 = 1
else:
    value_21 = 0
    try:
        d2 = np.load('scale_up_results_without_21_' + fname + '.npz')
        vs_without = d2['vs']
        ks2 = d2['ks']
        if 'v21' in d2:
            value_21 = d2['v21']
    except IOError:
        vs_without = []
        ks2 = []

    try:
        d1 = np.load('scale_up_results_' + fname + '.npz')
        ks1 = d1['ks']
        vs = d1['vs']
        value_21 = vs[0] # in case the above file doesn't have it
    except IOError:
        vs = []
        ks1 = []

    try:
        o = np.load('expected_split_' + fname + '.npz')
        rand_value = o['average_value']
    except IOError:
        rand_value = 0

# construct bounds
bounds2 = two_round_bounds(ks2, value_21, vs_without)
approx2 = approx_two_round_bounds(ks2, value_21, vs_without)

bounds1 = one_round_bounds(ks1, vs)
approx1 = approx_one_round_bounds(ks1, vs)

# print out stats for 2 round version
print("2 round bound:")
print('k', '\tfraction')
nkk = min(15, len(bounds2))
for k in range(1, nkk+1):
    print(k, "\t{:.4f}".format(bounds2[k-1]/rand_value))
bd, i = max(zip(bounds2, ks2))
print('best bound at', i, 'with fraction', "{:.4f}".format(bd /rand_value))
bd, i = max(zip(approx2, ks2))
print('best approx at', i, 'with fraction', "{:.4f}".format(bd/rand_value))


# do plot
ks = ks1 if ks1.size > ks2.size else ks2

plt.plot(ks2, vs_without, label='mean (2k, k) value without assignments in (2, 1)')
plt.plot(ks1, vs, label='mean (2k, k) value', color='lightblue')
plt.plot(ks2, bounds2, label='bound, 2 round', color='pink')
plt.plot(ks2, approx2, label='approx bound, 2 round', color='red')
plt.plot(ks1, bounds1, label='bound, 1 round', color='gold')
plt.plot(ks1, approx1, label='approx bound, 1 round', color='orange')
plt.plot(ks, [rand_value] * len(ks), label='actual random split expectation', linestyle='--')
plt.plot(ks, [value_21] * len(ks), label='actual optimal value', linestyle='--')
plt.xlabel('k')
plt.ylabel('mean assignment value')
plt.ylim(bottom=0)
plt.legend()
plt.title(fname)
plt.savefig('bounds_' + fname + '.png')
plt.show()
plt.close()

