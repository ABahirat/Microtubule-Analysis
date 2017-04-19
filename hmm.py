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
def train_hmm():
    input_file = raw_input("Input file to use for training: ")
    raw_input("Press enter to continue...")

######################################################################################
# Viterbi Function
#   Runs viterbi using previously calculated probabilities
#   Prints out accuracy calculations
#
#   Returns None
#
######################################################################################
#def viterbi():
#    input_file = raw_input("Input file to run viterbi on: ")
#    raw_input("Press enter to continue...")

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
