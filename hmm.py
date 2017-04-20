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

    for i in range(length_height):
        pair_list.append((-99999.,-99999)) # using -999 as start state/value
        for j in range(len(length_matrix[0])):
            pair_list.append((length_matrix[i][j],state_matrix[i][j]))
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
    training[emissions] = emission prob
    return training #returns a dictionary with set of states, and the start, transition and emission probabilities

    #outputs a list:
    # index 0
    




            
    
    
                

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
def viterbi():
    input_file = raw_input("Input file to run viterbi on: ")
    raw_input("Press enter to continue...")

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

    return

######################################################################################
# Call of main function starting the program
#
######################################################################################
if __name__ == "__main__":
    main(sys.argv[1:])
