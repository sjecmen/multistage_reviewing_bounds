import numpy as np

def load_sims(fname):
    d = np.load(fname + '.npz')
    S = d['similarity_matrix']
    M = d['mask_matrix']
    S[M == 1] = 0
    return S, M
