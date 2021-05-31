import numpy as np
import gurobipy as gp
from gurobipy import GRB

rng = np.random.default_rng()

'''
Calculate maximum-similarity assignment and return value
    S : similarity matrix
    M : conflict matrix
    revloads : vector or int of reviewer load limits
    paploads : vector or int of paper load requirements
'''
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

'''
Calculate value of a random split and of the optimum for that paper sample
    S : similarity matrix
    M : conflict matrix
    revload : reviewer load in each stage
    papload : paper load in each stage
    c : fraction of stage two papers
    opt : True if optimum should be calculated
'''
def split_assignment(S, M, revload, papload, c, opt=True):
    P2 = sample_second_stage_papers(S.shape[1], c)
    if opt:
        x_opt = opt_assignment_with_papers(S, M, revload, papload, P2)
    else:
        x_opt = None
    x_split = split_assignment_with_papers(S, M, revload, papload, P2)
    return x_split, x_opt

'''
Sample cn of the n papers
'''
def sample_second_stage_papers(n, c):
    return rng.choice(n, int(c * n), replace=False)

'''
Calculate the optimal value for a given stage two paper set P2
'''
def opt_assignment_with_papers(S, M, revload, papload, P2):
    opt_paper_loads = np.full((S.shape[1]), papload)
    for p in P2:
        opt_paper_loads[p] += papload

    opt_val, _ = match(S, M, revload, opt_paper_loads)
    return opt_val

'''
Sample the random split value for a given stage two paper set P2
'''
def split_assignment_with_papers(S, M, revload, papload, P2):
    c = len(P2) / S.shape[1]

    revs = list(range(S.shape[0]))
    rng.shuffle(revs) 
    splitrev = int(S.shape[0] / (1+c))
    R1 = revs[:splitrev]
    R2 = revs[splitrev:]

    S1 = S[R1, :]
    S2 = S[R2, :][:, P2]
    M1 = M[R1, :]
    M2 = M[R2, :][:, P2]
    x1,_ = match(S1, M1, revload, papload)
    x2,_ = match(S2, M2, revload, papload)
    return x1 + x2
