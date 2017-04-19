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
import sys, getopt, operator
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

    if len(opts) != 4 or len(opts) != 0: # Needs two arguments to run
        print('Invalid number of arguments')
        print_usage()
        sys.exit(0)

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

    print("Data File:\t{0}".format(data_file))
    print("Training File:\t{0}".format(training_file))
    print("Algorithm:\t{0}".format(algorithm))
    print
    
    return

######################################################################################
# Call of main function starting the program
#
######################################################################################
if __name__ == "__main__":
    main(sys.argv[1:])
