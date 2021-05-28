import numpy as np
from load_sims import *
import matplotlib.pyplot as plt
from bounds import *
import sys
from scipy.stats import sem

''' 
Plots bounds for both the 2 round and 1 round in-expectation bounds. 
Uses input from the scale_up_assignment, scale_up_assignment_without_21, and get_expected_split_value files if available. 
Assumes c=1 for both.
'''

fname = sys.argv[1]
max_k = 20

fontsize = 18
markersize=10
lw=3
colors = ['blue', 'red', 'orange']
ls = ['dashed', 'solid', 'solid']
labels = ['Random split expectation', 'Theorem 6 bound', 'Theorem 7 bound']
markers = ["", "s", "^"]

if fname=='legend':
    plt.figure(figsize=(10, 5))
    plt.rcParams.update({'font.size': 10})
    for i in range(3):
        plt.plot(np.arange(10), np.zeros(10), label=labels[i], color=colors[i], marker=markers[i], ms=markersize, linewidth=lw, linestyle=ls[i])
    plt.legend(ncol=3, handlelength=4)
    plt.savefig("legend_full.pdf")
    quit()
else:
    value_21 = 0
    try:
        d2 = np.load('scale_up_results_without_21_' + fname + '.npz')
        vs_without = d2['vs'][:max_k]
        ks2 = d2['ks'][:max_k]
        if 'v21' in d2:
            value_21 = d2['v21']
    except IOError:
        vs_without = []
        ks2 = []

    try:
        d1 = np.load('scale_up_results_' + fname + '.npz')
        ks1 = d1['ks'][:max_k]
        vs = d1['vs'][:max_k]
        value_21 = vs[0] # in case the above file doesn't have it
    except IOError:
        vs = []
        ks1 = []

    try:
        o = np.load('expected_split_' + fname + '.npz')
        rand_value = o['average_value']
        samples = o['samples']
        rand_sem = sem(samples)
    except IOError:
        rand_value = 0

# construct bounds
#bounds2 = two_round_bounds(ks2, value_21, vs_without, True)
approx2 = two_round_bounds(ks2, value_21, vs_without, False)
bestv2, bestk2 = max(zip(approx2, ks2))

#bounds1 = one_round_bounds(ks1, vs, 1, True)
approx1 = one_round_bounds(ks1, vs, 1, False)
bestv1, bestk1 = max(zip(approx1, ks1))


for i in range(len(ks2)):
    print(i+1)
    print(approx2[i] / rand_value)

# do plot
ks = ks1 if len(ks1) > len(ks2) else ks2

plt.rcParams.update({'font.size': fontsize})
plt.plot(ks, [rand_value] * len(ks), label=labels[0], color=colors[0], marker=markers[0], linestyle=ls[0], linewidth=lw, ms=markersize)
plt.fill_between(ks, [rand_value-rand_sem] * len(ks), [rand_value+rand_sem] * len(ks), color='lightblue')
#plt.plot(ks, [rand_value-rand_sem] * len(ks), color='lightblue', marker=markers[0], ms=markersize)
#plt.plot(ks, [rand_value+rand_sem] * len(ks), color='lightblue', marker=markers[0],  ms=markersize)
plt.plot(ks1, approx1, label=labels[1], color=colors[1], linestyle=ls[1], marker=markers[1], linewidth=lw, ms=markersize)
plt.plot(ks2, approx2, label=labels[2], color=colors[2], linestyle=ls[2], marker=markers[2], linewidth=lw, ms=markersize)
#plt.plot(ks2, vs_without, label='mean (2k, k) value without assignments in (2, 1)')
#plt.plot(ks1, vs, label='mean (2k, k) value', color='lightblue')
#plt.plot(ks2, bounds2, label='bound, 2 round', color='pink')
#plt.plot(ks1, bounds1, label='bound, 1 round', color='gold')
#plt.plot(ks, [value_21] * len(ks), label='actual optimal value', linestyle='--')
plt.plot(bestk1, bestv1, markeredgecolor='black', marker='o', ms=markersize*3, markerfacecolor='none')
plt.plot(bestk2, bestv2, markeredgecolor='black', marker='o', ms=markersize*3, markerfacecolor='none')
plt.xlabel('Benchmark assignment load parameter (\u03BC)')
plt.ylabel('Average assignment value')
plt.ylim(bottom=0)
#plt.legend()
plt.tight_layout()
plt.savefig('bounds_' + fname + '.pdf')
plt.show()
plt.close()

