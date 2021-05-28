import numpy as np
import json
import string
from LP import *


second_round_fracs = [0.1, 0.5]
# top or mid
part = 'mid'


def find_paper_index(url, paper_idx):
# takes the full url of a paper and returns its corresponding index using the iclr2018 paper_idx table
    url_suffix = url.split("=")[-1]
    key = url_suffix + ".txt"

    if key in paper_idx:
        return paper_idx[key]
    return None


# remove papers not in the iclr2018 similarities dataset
def filter_papers(final_json, paper_idx):
# returns list of paper information, but only for papers in our iclr2018.npz set
    filtered_data = []
    data = [i for i in final_json]

    for point in data:
        index = find_paper_index(point["url"], paper_idx)
        
        if index is not None:
            filtered_data.append(point)
    
    return filtered_data

def get_accept_fraction(filtered_data):
    # Get the fraction of accepted papers
    proper = [i for i in filtered_data if 'decision' in i]
    print("proper len", len(proper))

    accept_count = 0
    for i in proper:
        if i['decision'][:6] == "Accept":
            accept_count += 1

    print("accepts", accept_count)
    return accept_count/len(proper)


def get_second_round_papers(threshold, filtered_data):
    lower = int(len(filtered_data) * threshold[0])
    upper = int(len(filtered_data) * threshold[1])
    papers_slice = filtered_data[int(lower):int(upper)]

    chosen = []
    for paper in papers_slice:
        chosen.append(find_paper_index(paper['url'], paper_idx))
    return chosen



# load json file containing ratings
f = open('datasets/iclr2018.json', 'r')
final_json = json.loads(f.read())
f.close()


# load the iclr2018.npz similarities and paper index map
dataset = np.load("datasets/iclr2018.npz", allow_pickle = True)
paper_idx = dataset["paper_idx"][()]
S = dataset["similarity_matrix"]
M = dataset["mask_matrix"]
S[M == 1] = 0
revs, paps = S.shape

filtered_data = filter_papers(final_json, paper_idx)
accept_fraction = get_accept_fraction(filtered_data)

papload = 2
revload = 6
results = {c : [] for c in second_round_fracs}
opt_results = {c:[] for c in second_round_fracs}
T = 10

for portion in second_round_fracs:
    if part == 'mid':
        threshold = (accept_fraction - portion/2, accept_fraction + portion/2, portion)
    elif part == 'top':
        threshold = (0, portion, portion)
    
    P2 = get_second_round_papers(threshold, filtered_data)
    print(len(P2))
    assert(len(P2) == int(portion * S.shape[1]))

    #v, v_opt = split_assignment(S, M, revload, papload, threshold[2], second_round_paper_set)
    v_opt = opt_assignment_with_papers(S, M, revload, papload, P2)
    print('opt', v_opt)
    opt_results[portion].append(v_opt)
    for t in range(T):
        v = split_assignment_with_papers(S, M, revload, papload, P2)
        results[portion].append(v)
        print(t, v)

np.savez('split_samples_score_'+part+'.npz', opt_samples=opt_results, split_samples=results, revload=revload, papload=papload)
