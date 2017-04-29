import matplotlib.pyplot as plt
import os

# Initialize different types of bins
bins = []
bins.append([-0.2,0.0,0.2])
bins.append([-0.2,-0.1,0.0,0.1,0.2])
bins.append([-0.3,-0.1,0.0,0.1,0.3])
bins.append([-0.3,-0.2,0.0,0.2,0.3])
bins.append([-0.4,-0.2,0.0,0.2,0.4])
bins.append([-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3])
bins.append([-0.3,-0.25,-0.2,-0.15,-0.1,-0.05,0.0,0.05,0.1,0.15,0.2,0.25,0.3])

# Set different length files
length_files = []
length_files.append('singles_lengths_1.csv')
length_files.append('singles_lengths_2.csv')
length_files.append('doubles_lengths_1.csv')
length_files.append('doubles_lengths_2.csv')
length_files.append('long_lengths.csv')

# Set different state files
state_files = []
state_files.append('singles_states_1.csv')
state_files.append('singles_states_2.csv')
state_files.append('doubles_states_1.csv')
state_files.append('doubles_states_2.csv')
state_files.append('long_states.csv')

# Binning function to round values into bins
def bin(value,bins):
    best = 999999
    dist = 999999
    for i in range(len(bins)):
        new = abs(bins[i] - value)
        if(abs(new) < dist):
            best = bins[i]
            dist = abs(new)
    return best

def generate_state_distrobutions():
    # Calculate distrobutions in state files
    for state_file in state_files:
        
        # Get states from file
        states = []
        with open('data/'+state_file, 'r') as sf:
            states_raw = []
            for line in sf:
                states_raw  = line.split(',')
                states = states + [int(i) for i in states_raw]

        # Get unqiue values in states to see what states possible
        states_set = list(set(states))

        # Count number of each of the possible states 
        counts = [states.count(i) for i in states_set]

        # Create bar grah
        state_file = state_file[:-4] # Remove .csv from name
        plt.bar(states_set, counts, align='center', alpha=0.5)
        plt.xticks(states_set)
        plt.xlabel('States')
        plt.title('State Distrobution For File \''+state_file+'\'')
        plt.savefig('plots/state_distrobutions/'+state_file+'_distrobution.png')
        plt.clf() # clear figure

def generate_length_distrobutions():
    # Calculate distrobutions in bin files
    for length_file in length_files:
        
        bin_number = 0
        # Run every bin on each file
        for data_bin in bins:
            lengths = []
            lengths.append(0)
            # Get lengths from file
            with open('data/'+length_file, 'r') as lf:
                lengths_raw = []
                for line in lf:
                    length_raw  = line.split(',')
                    for i in range(1,len(length_raw)): # Find differences between value before
                        lengths = lengths + [bin(float(length_raw[i])-float(length_raw[i-1]),data_bin)]

            # Get possible bins
            lengths_set = data_bin

            # Count number of each of the possible states 
            counts = [lengths.count(i) for i in lengths_set]

            # Remove .csv form name
            length_file_clean = length_file[:-4]

            # Make incrementing list to size of length set for x position
            x_position = list(range(0,len(lengths_set)))

            # Create bar grah
            plt.bar(x_position, counts, align='center', alpha=0.5)
            plt.xticks(x_position,lengths_set)
            plt.xlabel('Bins')
            plt.title('Bin Distrobution For File \''+length_file_clean+'\' with bin '+str(bin_number))
            plt.savefig('plots/length_distrobutions/'+length_file_clean+'_bin-'+str(bin_number)+'_distrobution.png')
            plt.clf() # clear figure

            bin_number += 1

def generate_length_state_distrobutions():
    # This would do the same thing as 'generate_length_distrobutions()' except the bar graphs would have
    # each of the bars made up of the number of each of the states it is made up of.
    # For example if 30 samples belonged to bin 0.0, the bar for that bin would be made up of 3 sections,
    # one section for each possible state, showing how much of each of the things in that bin are made up of which states 
    return

def generate_probability_tables():
    # Generate nice looking emission and transion probability tables
    return

def generate_bin_accuracy():
    # Generate plots showing viterbi accuracy of each bin
    return

def exit_program():
    print("Exiting!")
    exit(0)

def run_all():
    print("~Generating state distrobution plots...")
    generate_state_distrobutions()
    print("~Generating length distrobution plots...")
    generate_length_distrobutions()
    print("~Generating length state distrobution plots...")
    generate_length_state_distrobutions()
    print("~Generating probability tables...")
    generate_probability_tables()
    print("~Generating bin accuracy plots...")
    generate_bin_accuracy()
    return

def print_menu_options():
    print("---Analytics program for microtubule hmm project---")
    print("Menu Options:")
    print("1: Generate State Distrobution Plots")
    print("2: Generate Length Distrobution Plots")
    print("3: Generate Length State  Distrobution Plots")
    print("4: Generate Probability Tables Distrobution Plots")
    print("5: Generate Generate Bin Distrobution Plots")
    print("6: Run All")
    print("0: Exit")

menu_actions = {
    '0' : exit_program,
    '1' : generate_state_distrobutions,
    '2' : generate_length_distrobutions,
    '3' : generate_length_state_distrobutions,
    '4' : generate_probability_tables,
    '5' : generate_bin_accuracy,
    '6' : run_all,
}

# Run using menu
os.system('clear')
while True:
    print_menu_options()
    choice = raw_input(">>  ")
    try:
        menu_actions[choice]()
        choice = raw_input("Finished! Press Enter to continue...")
        os.system('clear')                                                                                                    
    except KeyError:
        os.system('clear')
        print "Invalid selection, please try again.\n"
