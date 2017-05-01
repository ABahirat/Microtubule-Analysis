cd ..
python hmm.py -L data/singles_lengths_noise_1.csv -S data/singles_states_1.csv -O data/singles_lengths_noise_2.csv -T data/singles_states_2.csv -A viterbi -B -0.2,0.0,0.2
