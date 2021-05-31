import numpy as np

'''
Load similarity and conflicts, setting conflicted similarities to 0
'''
def load_sims(fname):
    d = np.load(fname + '.npz')
    S = d['similarity_matrix']
    M = d['mask_matrix']
    S[M == 1] = 0
    return S, M

'''
Duplicate reviewers so that there are at least 2 * npap reviewers. Split the similarity set
between the copies evenly, in paper-index order.
'''
def scale_reviewers(S):
    nreviews = 2 * S.shape[1]
    revscale = int(np.ceil(nreviews / S.shape[0]))
    if revscale == 1:
        return S, revscale
    splits = np.array_split(S, revscale, axis=1)
    newS = np.zeros((S.shape[0] * revscale, S.shape[1]))
    i = 0
    j = 0
    for x in range(revscale):
        split = splits[x]
        ni = i + split.shape[0]
        nj = j + split.shape[1]
        newS[i:ni, j:nj] = split
        i = ni
        j = nj
    assert(newS.shape[0] >= 2 * newS.shape[1])
    assert(np.all(np.sum(S, axis=0) == np.sum(newS, axis=0)))
    return newS, revscale

