import numpy as np
import matplotlib.pyplot as plt
from load_sims import *
import sys

'''
Plot sampled random splits.
Uses input from the get_split_samples or get_split_samples_score files.
Command line arg: 'main' (random P2, results in main paper), 'supp' (random P2, results in appendix), or 'scores' (score-based P2, results in main paper)
'''

which = sys.argv[1]
if which == 'main':
    fnames = ['iclr2018', 'preflib3', 'DA1', 'query']
    nicefnames = ['ICLR', 'PrefLib3', 'Bid1', 'SIGIR']
    figsize=(12, 6)
    cs = {f:[0.1, 0.5] for f in fnames}
elif which == 'supp':
    fnames = ['iclr2018', 'preflib3', 'DA1', 'query', 'preflib1', 'preflib2', 'DA2']
    nicefnames = ['ICLR', 'PrefLib3', 'Bid1', 'SIGIR', 'PrefLib1', 'PrefLib2', 'Bid2']
    figsize=(18, 6)
    cs = {fnames[i]:[0.3] if i < 4 else [0.1, 0.3, 0.5] for i in range(7)}
elif which == 'scores':
    fnames = ['score_top', 'score_mid']
    nicefnames = ['Top', 'Middle']
    figsize=(8, 6)
    cs = {f:[0.1, 0.5] for f in fnames}
else:
    assert(False)

xs = []
minys = []
maxys=[]
ticks = []
labels = []
idx = 0

for fname, nicefname in zip(fnames, nicefnames ):
    infilename = 'split_samples_'+fname+'.npz'
    d = np.load(infilename, allow_pickle=True)
    opt_data = d['opt_samples'][()]
    split_data = d['split_samples'][()]

    for c in cs[fname]:
        if which == 'scores':
            percents = [s/opt_data[c][0] for s in split_data[c]]
        else:
            percents = [s/o for o, s in zip(opt_data[c], split_data[c])]
        xs.append(idx)
        minys.append(min(percents))
        maxys.append(max(percents))
        ticks.append(idx)
        labels.append(nicefname + '\n\u03B2=' + str(c))
        idx += 1 

print(minys)
plt.rcParams.update({'font.size': 16})
plt.figure(figsize=figsize)
plt.tight_layout()
plt.plot((xs, xs), (minys, maxys), '-', color='black', solid_capstyle="butt", linewidth=5)
plt.scatter(xs, minys, 100, color='black', marker='_')
plt.scatter(xs, maxys, 100, color='black', marker='_')
plt.ylim(bottom=0, top=1)
plt.xticks(ticks=ticks, labels=labels)
plt.ylabel('Fraction of optimal similarity', fontsize=22)
plt.savefig(which + '_exp.pdf')
plt.show()
