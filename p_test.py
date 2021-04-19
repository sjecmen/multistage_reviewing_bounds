import numpy as np
import matplotlib.pyplot as plt
from bounds import *

'''
Run some tests and plot results of the values of p against their approximatinos.
'''

nk = 100
ks = list(range(1, nk+1))

approx2 = approx_two_round(ks)
approx2 = np.maximum(0, approx2)
ps2 = []
print('2 round')
max_c = 0
for k in ks:
    p = p_two_round(k)
    c = np.sqrt(k) * (1 - p)
    max_c = max(c, max_c)
    if k <= 20:
        print(k, "{:.4f}".format(max_c))
    ps2.append(p)
print('num actual below approx', np.sum(np.asarray(ps2) < approx2))

approx1 = approx_one_round(ks)
ps1 = []
print('1 round')
max_c = 0
for k in ks:
    p = p_one_round(k)
    c = np.sqrt(k) * (1 - p)
    max_c = max(c, max_c)
    if k <= 20:
        print(k, "{:.4f}".format(max_c))
    ps1.append(p)
print('num actual below approx', np.sum(np.asarray(ps1) < approx1))


plt.plot(ks, ps2, label='actual, 2 round')
plt.plot(ks, approx2, label='approx, 2 round')
plt.plot(ks, ps1, label='actual, 1 round')
plt.plot(ks, approx1, label='approx, 1 round')
plt.title('p with gaussian approximations')
plt.legend()
plt.savefig('p_test.png')
plt.show()
