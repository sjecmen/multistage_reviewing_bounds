import numpy as np
import gurobipy as gp
from gurobipy import GRB

rng = np.random.default_rng()

def match(S, M, revloads, paploads):
    if type(revloads) == int:
        revloads = np.full(S.shape[0], revloads)
    if type(paploads) == int:
        paploads = np.full(S.shape[1], paploads)

    model = gp.Model("my_model") 
    model.setParam('OutputFlag', 0)
    obj = 0
    n, d = S.shape
    assert len(revloads) == n and len(paploads) == d and S.shape == M.shape
    review_demand = np.sum(paploads)
    review_supply = np.sum(revloads)

    if review_demand > review_supply:
        print('infeasible assignment')
        raise RuntimeError('infeasible')

    A = [[None for j in range(d)] for i in range(n)]

    for i in range(n):
        for j in range(d):
            if (M[i, j] == 1):
                v = model.addVar(lb = 0, ub = 0, name = f"{i} {j}")
            else:
                v = model.addVar(lb = 0, ub = 1, name = f"{i} {j}") 
                
            A[i][j] = v
            obj += v * S[i, j]

    model.setObjective(obj, GRB.MAXIMIZE)
    
    for i in range(n):
        papers = 0
        for j in range(d):
            papers += A[i][j]
        model.addConstr(papers <= revloads[i]) 
    
    for j in range(d):
        reviewers = 0
        for i in range(n):
            reviewers += A[i][j]
        model.addConstr(reviewers == paploads[j])
    
    model.optimize()

    if model.status != GRB.OPTIMAL:
        print("WARNING: model not solved")
        raise RuntimeError('unsolved')

    B = [[None for j in range(d)] for i in range(n)]
    for i in range(n):
        for j in range(d):
            B[i][j] = A[i][j].x

    return model.objVal, B 

def comp_value(S, A):
    v = 0
    for i in range(S.shape[0]):
        for j in range(S.shape[1]):
            v += S[i, j] * A[i][j]
    return v


def split_assignment(S, M, k, l, frac):
    
    # get the reviewers split up based on frac proportion
    revs = list(range(S.shape[0]))
    rng.shuffle(revs)
    halfrevs = int(S.shape[0] / (1 + frac))
    R1 = revs[:halfrevs]
    R2 = revs[halfrevs:]

    # get the first and second round paper sets
    paps = list(range(S.shape[1]))
    rng.shuffle(paps)
    halfpaps = int(S.shape[1] * frac)
    P1 = paps
    P2 = paps[:halfpaps]

    S1 = (S[R1, :])[:, P1]
    S2 = (S[R2, :])[:, P2]
    M1 = (M[R1, :])[:, P1]
    M2 = (M[R2, :])[:, P2]

    x1,A1 = match(S1, M1, np.full((S1.shape[0]), k), np.full((S1.shape[1]), l))
    x2,A2 = match(S2, M2, np.full((S2.shape[0]), k), np.full((S2.shape[1]), l))

    pap_loads_opt = np.full((S.shape[1]), l)
    for pap in P2:
        pap_loads_opt[pap] += l
    
    x3,A3 = match(S, M, np.full((S.shape[0]), k), pap_loads_opt)

    return x1 + x2, x3