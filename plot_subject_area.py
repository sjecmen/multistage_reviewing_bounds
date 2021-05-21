import numpy as np
import matplotlib.pyplot as plt

d = np.load('subject_area_data_2.npz', allow_pickle=True)
opt_data = d['opt_data'][()]
split_data = d['split_data'][()]
ns = d['ns']

c=0.5
ol = []
os = []
sl = []
ss = []
l = []
ov = opt_data[c]
sv = split_data[c]
for i in range(len(ov)):
    ol.append(ov[i][0])
    os.append(ov[i][1])
    sl.append(sv[i][0])
    ss.append(sv[i][1])
    l.append(ov[i][0] - sv[i][0])

fontsize = 14
markersize=7
lw=3
plt.rcParams.update({'font.size': fontsize})

fig, ax1 = plt.subplots()
ax1.set_xlabel('Number of reviewers and papers')
ax1.set_ylabel('Average similarity')
ax1.errorbar(ns, ol, yerr=os, linewidth=lw, ms=markersize, marker='s', label='Optimal')
ax1.errorbar(ns, sl, yerr=ss, linewidth=lw, ms=markersize, marker='^', label='Random split')
ax1.set_ylim(bottom=0)


ax2 = ax1.twinx()
ax2.set_ylabel('Suboptimality of average similarity')
ax2.plot(ns, l, linestyle='dashed', linewidth=lw, color='pink', label='Suboptimality')

fig.tight_layout()
z = 0.17
fig.legend(loc=(z, z))
plt.savefig('subject_area.pdf')
plt.show()


