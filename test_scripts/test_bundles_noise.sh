cd ..
python hmm.py -L data/bundles_lengths_noise_1.csv -S data/bundles_states_1.csv -O data/bundles_lengths_noise_2.csv -T data/bundles_states_2.csv -A viterbi -B -0.2,0.0,0.2
