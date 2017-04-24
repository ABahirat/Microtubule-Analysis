######################################################################################
#   File            : hmm.py
#   Purpose         : Hidden Markov Model for microtuule analysis
#   Developer       : Thomas Lillis, Ameya Bahirat, Robert Ballard
######################################################################################
#   
#   Sample command line arguments to run program: 
#
#       python hmm.py -D test.data -T training.data -A viterbi
#
#   -D specifies the testing data
#   -T specifies the training file
#   -A specifies the scoring file to be used
#
######################################################################################
#   
#   Algorithm Explanation: 
#       
#
######################################################################################
# 
#   References: Alex Okeson Jan 2016
#               alexokeson_hw1.py
#               Formatting of the header comment
#
######################################################################################
import os, sys, getopt, operator
import numpy as np
from sklearn.metrics import f1_score, classification_report, confusion_matrix


######################################################################################
# Print Usage Function
#   Prints proper way to use program when arguments are incorrect
#
#   Returns None
#
######################################################################################
def print_usage():
    print 'hmm.py -D <data file> -T <training file> -A <algorithm>'
    return

######################################################################################
# Handle Args Function
#   Takes command line arguments and returns the correctly populated variables
#   Prints out usage if incorrectly formatted
#
#   Returns the file name
#
######################################################################################
def handle_args(argv):
    try:
        opts, args = getopt.getopt(argv,"hD:d:T:t:A:a:")
    except getopt.GetoptError:
        print_usage()
        sys.exit(0)

    if len(opts) != 4 and len(opts) != 0: # Needs two arguments to run
        print(len(opts))
        print('Invalid number of arguments')
        print_usage()
        sys.exit(0)

    data_file = None
    training_file = None
    algorithm = None

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-D", "-d"):
            data_file = arg
        elif opt in ("-T", "-t"):
            training_file = arg
        elif opt in ("-A", "-a"):
            algorithm = arg
        else:
            print("Unknown argument option: {0}".format(opt))
            print_usage()
            exit(0)

    return data_file, training_file, algorithm

######################################################################################
# Print Menu Options Function
#   Prints menu options
#
#   Returns None
#
######################################################################################
def print_menu_options():
    print "HMM Microtubule Analysis"
    print "1: Train"
    print "2: Viterbi"
    print "3: Exit"
    return

######################################################################################
# Bin Function
#   Given some float, will return a binned float in the set of bins currently in use
#
#   Returns binned float
#
######################################################################################
def bin(value):
    bins = [-0.2,-0.1,0.0,0.1,0.2]
    best = 999999
    dist = 999999
    for i in range(len(bins)):
        new = abs(bins[i] - value)
        if(abs(new) < dist):
            best = bins[i]
            dist = abs(new)
    return best

######################################################################################
# Train HMM Function
#   Train hmm on data file
#
#   Returns training probabilities
#
######################################################################################
def do_train(flengths, fstates):
    pair_list = []
    length_matrix = []
    state_matrix = []
    length_height = 0
    state_height = 0
    print "Parsing file..."

    with open(flengths, 'r') as lengths:
        with open(fstates, 'r') as states:
            for line in lengths:
                length_height += 1
                length_matrix.append(line.split(','))
            for line in states:
                state_height += 1
                state_matrix.append(line.split(','))

    if length_height != state_height or len(length_matrix[0]) != len(state_matrix[0]):
        print "matrices not same size"
        exit(0)

    for i in range(length_height-1):
        pair_list.append((-99999.,-99999)) # using -999 as start state/value
        for j in range(len(length_matrix[0])):
            newlength = bin(length_matrix[i+1][j] - length_matrix[i][j]) #get diff of lengths and bin
            pair_list.append((newlength,state_matrix[i][j]))
        pair_list.append((99999.,99999)) # using 999 as end state/value
    
    print "Done parsing..."
    
    transition_prob = {}
    emission_prob = {}
    start_prob = {}
    states_data = {}
    lengths_data = {}
    states_count = {} #contains count of each state
    states_set = set()
    lengths_set = set()

    print "Storing occurences of states in dictionary... "

    for length, state in pair_list:
        if state not in state_count.keys():
            stateCount = 0
            for length1, state1 in pair_list:
                if state = state1:
                    stateCount += 1
                state_count[state] = stateCount
        states_set.add(state)
        lengths_set.add(length)

    print "Creating starting probabilities...  "

    for state in states_set:
        if state == -99999:
            start_prob[state] = 1
        else:
            start_prob[state] = 0

    print "Creating dictionaries..."

    for state in states_set:
        if state not in state_data.keys():
            state_data[state] = {}
            transition_prob[state] = {}
        for state1 in states_set:
            if state1 not in state_data[state] and state1 not in transition_prob[state]: #if state combination does not exist
                state_data[state][state1] = 0
                transition_prob[state][state1] = 0

    for length in lengths_set:
        #if state not in length_data.keys() and state not in emission_prob.keys():
        length_data[length] = {}
        #emission_prob[state] = {}
        for state in states_set:
          # if length not in length_data[length] and state not in emission_prob[state]:
            emission_prob[state] = {}
            length_data[length][state] = 0
            emission_prob[state][length] = 0

    print "Appending values to dictionaries... "

    for length, state in pair_list:
        
        length_data[length][state]+=1

    for x in range(0, len(pair_list)):
        if x == len(pair_list) -1:
            break
        first_state = pair_list[x][1]
        second_state = pair_list[x+1][1]
        state_data[first_state][second_state] +=1

    print "Storing emission and transition probabilities... "
            
    for state in states_set:
        for state1 in states_set:
            #if transition_prob[tag1][tag] == 0:
            transition_prob[state1][state] = float(state_data[state1][state])/float(state_count[state]) 

    for length in lengths_set:
        for state in states_set:
            #if emission_prob[tag][word] == 0:
            emission_prob[state][length] = float(length_data[length][state])/float(state_count[state])

    training = {}
    training[states] = states_set
    training[starts] = start_prob
    training[transitions] = transition_prob
    training[emissions] = emission_prob
    return training #returns a dictionary with set of states, and the start, transition and emission probabilities

def train_hmm():
    input_file = raw_input("Input lengths file to use for training: ")
    raw_input("Press enter to continue...")
    input_file2 = raw_input("Input states file to use for training: ")
    raw_input("Press enter to continue...")
    return do_train(input_file,input_file2)

######################################################################################
# Viterbi Function
#   Runs viterbi using previously calculated probabilities
#   Prints out accuracy calculations
#
#   Returns None
#
######################################################################################
def viterbi(obs, states, start_p, trans_p, emit_p): #stat_p, trans_p and emit_p all are dictionaries
    V = [{}] #V is a list of dictionaries, each of the dictionaries is a time which has a dictionary of states
    #Calculate V0, x for all states x, where 0 is time
    for st in states:
        #index = 0
        #if obs[0] in emit_p[st]:
         #   index = emit_p[st][obs[0]]
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
        #emit_p is pr(evidence | state), first dictionary contains key "prob" = start_pr for the state * emp_p for the state and "prev" none
        #obs is evidence at each time
        #obs[0] is Normal
        #V[0][st] = {"prob": start_p[st] * index, "prev": None} 
    # Run Viterbi when t > 0

    #print v[0][st] results in 
    for t in range(1, len(obs)): #loop through all observations, starting at second one, already looked at normal above
        V.append({}) #append dictionary to V
        for st in states:
            #v[t-1][prev_st]["prob"] is probability of being in prev_st at t-1
            #calculate previous time through loop
            #trans_p[prev_st][st] is transition probabilities
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states) #
            for prev_st in states: #incorporating evidence
                if V[t-1][prev_st]["prob"] * trans_p[prev_st][st] == max_tr_prob:
                    #emit_p[st][obs[t]] is emission probability of seeing observation in this state
                    #obst[t] is observation at time t
                    max_prob = max_tr_prob * emit_p[st][obs[t]]
                    #store V for time t in state st
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    for line in dptable(V):
        print line

    opt = []
    # The highest probability
    max_prob = max(value["prob"] for value in V[-1].values())
    previous = None
    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        #print st, data
        if data["prob"] == max_prob:
            opt.append(st)
            previous = st
            break
    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print 'The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob
######################################################################################
# Forward/Backward Algorithm
#
#
#
######################################################################################
def fwd_bkw(observations, states, start_prob, trans_prob, emm_prob, end_st):
    # forward part of the algorithm
    fwd = []
    f_prev = {}
    for i, observation_i in enumerate(observations):
        f_curr = {}
        for st in states:
            if i == 0:
                # base case for the forward part
                prev_f_sum = start_prob[st]
            else:
                prev_f_sum = sum(f_prev[k]*trans_prob[k][st] for k in states)

            f_curr[st] = emm_prob[st][observation_i] * prev_f_sum

        fwd.append(f_curr)
        f_prev = f_curr

    p_fwd = sum(f_curr[k] * trans_prob[k][end_st] for k in states)

    # backward part of the algorithm
    bkw = []
    b_prev = {}
    for i, observation_i_plus in enumerate(reversed(observations[1:]+(None,))):
        b_curr = {}
        for st in states:
            if i == 0:
                # base case for backward part
                b_curr[st] = trans_prob[st][end_st]
            else:
                b_curr[st] = sum(trans_prob[st][l] * emm_prob[l][observation_i_plus] * b_prev[l] for l in states)

        bkw.insert(0,b_curr)
        b_prev = b_curr

    p_bkw = sum(start_prob[l] * emm_prob[l][observations[0]] * b_curr[l] for l in states)

    # merging the two parts
    posterior = []
    for i in range(len(observations)):
        posterior.append({st: fwd[i][st] * bkw[i][st] / p_fwd for st in states})

    assert p_fwd == p_bkw
    return fwd, bkw, posterior

######################################################################################
# Calculate Metrics Function
#   
#
######################################################################################s
def calculate_metrics(results, truth_data):
    if len(results) != len(truth_data):
        print("Different lengths of results and truth data!")
        print("Results Length: {0}\t Truth Data Length: {1}".format(len(results),len(truth_data)))
        return

    results_len = len(results)

    # Calculate Accuracy
    correct = 0.0
    for i in range(results_len):
        if results[i] == truth_data[i]:
            correct += 1
    accuracy = correct/results_len
    print("Overall Accuracy:\t{0}".format(accuracy))

    # Calculate f-measure
    f1_macro = f1_score(truth_data, results, average='macro')
    f1_weighted = f1_score(truth_data, results, average='weighted')
    print("F-measure macro:\t{0}".format(f1_macro))
    print("F-measure weighred:\t{0}".format(f1_weighted))

    # Classification report
    report = classification_report(truth_data, results, digits=4)
    print("Report:\n{0}".format(report))

    # Confusion matrix
    matrix = confusion_matrix(truth_data,results)
    print("Confusion Matrix:")
    print(matrix)

    print("\nFinished results!")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return

######################################################################################
# Exit Program Function
#   Exits program
#
######################################################################################
def exit_program():
    print "Exiting!"
    exit()

######################################################################################
# Menu Actions Dictionary
#   Options for input into main menu
#
######################################################################################
menu_actions = {
        '1' : train_hmm,
        'train' : train_hmm,
        't' : train_hmm,
        '2' : viterbi,
        'viterbi' : viterbi,
        'v' : viterbi,
        '3' : exit_program,
        'exit' : exit_program,
        'q' : exit_program,
        'e' : exit_program,
}

######################################################################################
# Main Function
#   Calls functions to handle arguments, read in the sequences, and calculate alignments
#   and then with found distance matrix caculates tree using UPGMA
#
#   Returns None
#
######################################################################################
def main(argv):
    # Get command line arguments
    data_file,trainging_file,algorithm  = handle_args(argv)



    # Run using arguments
    if data_file:
        print("Data File:\t{0}".format(data_file))
        print("Training File:\t{0}".format(training_file))
        print("Algorithm:\t{0}".format(algorithm))
        print
        exit(0)
    
    # Run using menu
    os.system('clear')
    while True:
        print_menu_options()
        choice = raw_input(">>  ")
        try:
            menu_actions[choice]()
            os.system('clear')
        except KeyError:
            os.system('clear')
            print "Invalid selection, please try again.\n"

    calculate_metrics([0,0,0,0,0,0,1,2,3],[0,1,0,3,0,0,1,2,3])
    calculate_metrics([0,0,0],[0,1,0,3,0,0,1,2,3])
    calculate_metrics([0,1,0,3,0,0,1,2,3],[0,1,0,3,0,0,1,2,3])
    calculate_metrics([1,2,3,1,2,3,1,2,3],[1,2,3,1,2,3,1,2,3])


    return

######################################################################################
# Call of main function starting the program
#
######################################################################################
if __name__ == "__main__":
    main(sys.argv[1:])
