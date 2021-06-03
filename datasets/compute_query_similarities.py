import numpy as np

'''
Converts files from the Query dataset to our npz format.
'''

narea = 25
npap = 73
nrev = 189

R = np.zeros((nrev, narea))
P = np.zeros((npap, narea))

with open("Reviewers.txt") as infile:
    lines = infile.readlines()
    assert(len(lines) == nrev)
    for rev in range(nrev):
        toks = lines[rev].split()
        assert(rev == int(toks[0]) - 1)
        for i in range(1, len(toks)):
            assert(toks[i][0] == 'T')
            area = int(toks[i][1:]) - 1
            R[rev, area] = 1
    assert(np.all(np.sum(R, axis=1) >= 0))

with open("queryAspects.txt") as infile:
    lines = infile.readlines()
    assert(len(lines) == (npap * 2))
    for pap in range(npap):
        idx = (pap * 2) + 1
        toks = lines[idx].split()
        for tok in toks:
            assert(tok[0] == 'T')
            area = int(tok[1:]) - 1
            P[pap, area] = 1
    assert(np.all(np.sum(P, axis=1) >= 0))

S = R @ P.T
assert(S.shape == (nrev, npap))
S /= np.max(S)
assert(np.all(S <= 1) and np.all(S >= 0))
M = np.zeros_like(S)
np.savez('query.npz', similarity_matrix = S, mask_matrix=M)
