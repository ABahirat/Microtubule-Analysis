import matplotlib.pyplot as plt
import os
import hmm

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

def generate_state_distributions():
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
        plt.title('State Distribution For File \''+state_file+'\'')
        plt.savefig('plots/state_distributions/'+state_file+'_distribution.png')
        plt.clf() # clear figure

def generate_length_distributions():
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
                previous_end = None
                for line in lf:
                    length_raw  = line.split(',')
                    if previous_end: # Handle the previous lines last value minus first value of new line
                        lengths.append(hmm.bin(float(length_raw[0])-float(previous_end),data_bin))
                    previous_end = length_raw[-1]
                    for i in range(1,len(length_raw)): # Find differences between value before
                        lengths = lengths + [hmm.bin(float(length_raw[i])-float(length_raw[i-1]),data_bin)]

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
            plt.title('Bin Distribution For File \''+length_file_clean+'\' with bin '+str(bin_number))
            plt.savefig('plots/length_distributions/'+length_file_clean+'_bin-'+str(bin_number)+'_distribution.png')
            plt.clf() # clear figure

            bin_number += 1

def generate_length_state_distributions():
    # This would do the same thing as 'generate_length_distributions()' except the bar graphs would have
    # each of the bars made up of the number of each of the states it is made up of.
    # For example if 30 samples belonged to bin 0.0, the bar for that bin would be made up of 3 sections,
    # one section for each possible state, showing how much of each of the things in that bin are made up of which states

    for j in range(0, len(length_files)):

        bin_number = 0
        # Run every bin on each file
        for data_bin in bins:
            lengths = []
            lengths.append(0)
            # Get lengths from file
            with open('data/'+length_files[j], 'r') as lf:
                lengths_raw = []
                previous_end = None
                for line in lf:
                    length_raw  = line.split(',')
                    if previous_end: # Handle the previous lines last value minus first value of new line
                        lengths.append(hmm.bin(float(length_raw[0])-float(previous_end),data_bin))
                    previous_end = length_raw[-1]
                    for i in range(1,len(length_raw)): # Find differences between value before
                        lengths = lengths + [hmm.bin(float(length_raw[i])-float(length_raw[i-1]),data_bin)]
        
            # Get states from file

            states = []
            with open('data/'+state_files[j], 'r') as sf:
                states_raw = []
                for line in sf:
                    states_raw  = line.split(',')
                    states = states + [int(i) for i in states_raw]
                
            print('data/'+state_files[j]+'={0}'.format(len(states)))
            print('data/'+length_files[j]+'={0}'.format(len(lengths)))

            # Get unqiue values in states to see what states possible
            states_set = list(set(states))


            bin_states = {}

            for k in range(0,len(states)):
                if bin_states.has_key(str(states[k]) + "." + str(lengths[k])):
                    bin_states[str(states[k]) + "." + str(lengths[k])] += 1
                else: 
                    bin_states[str(states[k]) + "." + str(lengths[k])] = 1



            # Remove .csv form name
            length_file_clean = length_files[j][:-4]
            state_file = state_files[j][:-4]


            print bin_states.values()

            
            plt.bar(range(len(bin_states)), bin_states.values(), align='center')
            plt.xticks(range(len(bin_states)),bin_states.keys())
            plt.xlabel('Bins')
            plt.title('State Distribution For File \''+length_file_clean+'\' with bin '+str(bin_number))
            plt.savefig('plots/length_state_distributions/'+length_file_clean+'_bin-'+str(bin_number)+'_distribution.png')
            plt.clf() # clear figure
            bin_number += 1


        



    return

def generate_probability_tables():
    # Generate nice looking emission and transion probability tables

    bin_number = 0
    # Run every bin on each file
    for data_bin in bins:
        for i in range(len(length_files)):
            training = hmm.do_train('data/'+length_files[i],'data/'+state_files[i],data_bin)
            
            emissions = training['emissions']
            transitions = training['transitions']

            del emissions[99999]
            del emissions[-99999]
            del transitions[99999]
            del transitions[-99999]

            print("Building emission tables...")
            rows = []
            cell_text = []
            for key in emissions:
                rows.append(key)
                columns = []
                values = []
                del emissions[key][99999]
                del emissions[key][-99999]
                for key2 in emissions[key]:
                    columns.append(key2)
                    values = values + [emissions[key][key2]]
                cell_text.append(values)

            length_file_clean = length_files[i][:-4]
            state_file_clean = state_files[i][:-4]

            nrows, ncols = len(rows)+1, len(columns)
            hcell, wcell = 1.3, 2.
            hpad, wpad = 1, 1    
            fig=plt.figure(figsize=(ncols*wcell+wpad, nrows*hcell+hpad))
            ax = fig.add_subplot(111)
            ax.axis('off')

            plt.title('Probability table for \''+length_file_clean+'/'+state_file_clean+'\' with bin '+str(bin_number))
            the_table = ax.table(cellText=cell_text,
                              colLabels=columns,
                              rowLabels=rows,
                              loc='center')
            #plt.show()
            plt.savefig('plots/probability_tables/emission_'+length_file_clean+'-'+state_file_clean+'_bin-'+str(bin_number)+'.png')
            plt.clf() # clear figure

        bin_number += 1
    return

def generate_bin_accuracy():
    # Generate plots showing viterbi accuracy vs each bin

    bin_number = 0
    # Run every bin on each file
    for data_bin in bins:
        bin_number += 1
    return

def exit_program():
    print("Exiting!")
    exit(0)

def run_all():
    print("~Generating state distrobution plots...")
    generate_state_distributions()
    print("~Generating length distrobution plots...")
    generate_length_distributions()
    print("~Generating length state distrobution plots...")
    generate_length_state_distributions()
    print("~Generating probability tables...")
    generate_probability_tables()
    print("~Generating bin accuracy plots...")
    generate_bin_accuracy()
    return

def print_menu_options():
    print("---Analytics program for microtubule hmm project---")
    print("Menu Options:")
    print("1: Generate State Distribution Plots")
    print("2: Generate Length Distribution Plots")
    print("3: Generate Length State Distribution Plots")
    print("4: Generate Probability Tables Distribution Plots")
    print("5: Generate Generate Bin Distribution Plots")
    print("6: Run All")
    print("0: Exit")

menu_actions = {
    '0' : exit_program,
    '1' : generate_state_distributions,
    '2' : generate_length_distributions,
    '3' : generate_length_state_distributions,
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

