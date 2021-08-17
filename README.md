# Random Reviewer Splitting in Two-Stage Paper Assignment

Code to run simulations of random reviewer splits in two-stage paper assignment and calculate bounds. See the corresponding paper [here](https://arxiv.org/abs/2108.06371).

## Files 
- get_split_samples.py - takes samples of random split and the ex-post optimum split
- get_split_samples_score.py - takes samples of random split with stage-two papers chosen by score
- plot_main_data.py - plots the results (random split samples)

- scale_up_assignment.py - computes assignment values for Theorem 5 bound
- scale_up_assignment_without_21.py - computes assignment values for Theorem 6 bound
- get_expected_split_value.py - computes random split expected value
- plot_bounds.py - plots the results (bounds)

- load_sims.py - functions to load similarities
- LP.py - functions to compute assignments and take random splits
- bounds.py - functions to compute bounds
- expec_test.py - verifies that normal approximations used in bounds are actually lower bounds

- datasets/ - contains the similarity matrices used; sources:
	- [iclr2018.npz](https://github.com/xycforgithub/StrategyProof_Conference_Review)
	- [iclr2018.json](https://github.com/Chillee/OpenReviewExplorer)
	- [preflib*.npz](https://www.preflib.org/data/matching/csconf/) (transformed into similarities using compute_preflib_similarities.py)
	- [query.npz](http://sifaka.cs.uiuc.edu/ir/data/review.html) (called SIGIR in paper, transformed into similarities using compute_query_similarities.py)
