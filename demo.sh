## Script for running a demo

cost_matrix_file="data/example_cost_matrix.txt"
fanout=5
non_matching_cost=6.0
python3 img_seq_matcher.py ${cost_matrix_file} ${fanout} ${non_matching_cost}