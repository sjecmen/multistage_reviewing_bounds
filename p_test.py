import numpy as np
import matplotlib.pyplot as plt
from bounds import *
from itertools import product

'''
Run some tests and plot results of the values of p against their approximatinos.
'''

nk = 100#int(1e4)
ks = list(range(1, nk+1))
nc = 10
cs = [i/nc for i in range(1, nc+1)]

# verify that approximation is LB
# VERIFIED for k <= 25000, nc=100
exact_one = np.zeros((nk, nc))
approx_one = np.zeros((nk, nc))
print('1 round')
for i, j in product(range(nk), range(nc)):
    k = ks[i]
    c = cs[j]
    exact_one[i, j] = p_one_round(k, c, True)
    approx_one[i, j] = p_one_round(k, c, False)
    if exact_one[i, j] < approx_one[i, j]:
        print('1 round; k, c:', k, c)
        print('exact:', exact_one[i, j])
        print('approx:', approx_one[i, j])
    if k % 100 == 0 and c == 1:
        print(k)
assert(np.all(exact_one >= approx_one))

# VERIFIED for k <= 100000
exact_two = np.zeros((nk))
approx_two = np.zeros((nk))
print('2 round')
for i in range(nk):
    k = ks[i]
    exact_two[i] = p_two_round(k, True)
    approx_two[i] = p_two_round(k, False)
    if exact_two[i] < approx_two[i]:
        print('2 round; k:', k)
        print('exact:', exact_two[i])
        print('approx:', approx_two[i])
    if k % 100 == 0:
        print(k)
assert(np.all(exact_two >= approx_two))

ps2 = []
approx2 = []
print('2 round')
for k in ks:
    p = p_two_round(k, True)
    ap = p_two_round(k, False)
    ps2.append(p)
    approx2.append(max(ap, 0))
print('num actual below approx', np.sum(np.asarray(ps2) < np.asarray(approx2)))

ps1 = []
approx1 = []
print('1 round')
for k in ks:
    p = p_one_round(k, 1, True)
    ap = p_one_round(k, 1, False)
    ps1.append(p)
    approx1.append(ap)
print('num actual below approx', np.sum(np.asarray(ps1) < np.asarray(approx1)))


plt.plot(ks, ps2, label='actual, 2 round')
plt.plot(ks, approx2, label='approx, 2 round')
plt.plot(ks, ps1, label='actual, 1 round')
plt.plot(ks, approx1, label='approx, 1 round')
plt.title('p with gaussian approximations')
plt.legend()
plt.savefig('p_test.png')
plt.show()
