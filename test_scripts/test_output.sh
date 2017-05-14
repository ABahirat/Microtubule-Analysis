cd ..
python hmm.py -L data/bundles_lengths_1.csv -S data/bundles_states_1.csv -O data/bundles_lengths_2.csv -W data/test_ouput.csv -A viterbi -B -0.2,-0.1,0.0,0.1,0.2
