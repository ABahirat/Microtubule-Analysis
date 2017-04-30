import matplotlib.pyplot as plt
import os
import hmm
import numpy as np
import matplotlib.patches as mpatches

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
            lengths_set = data_bin

            for k in range(0, len(lengths_set)):
                bin_states[lengths_set[k]] = {}
                bin_states[lengths_set[k]][0] = 0
                bin_states[lengths_set[k]][1] = 0
                bin_states[lengths_set[k]][2] = 0

            for k in range(0,len(states)):
                bin_states[lengths[k]][states[k]] += 1


            # Remove .csv form name
            length_file_clean = length_files[j][:-4]
            state_file = state_files[j][:-4]

            
            
            x_position = list(range(0,len(lengths_set)))


            #print bin_states;
            n_groups = len(x_position)
            opacity = 0.7
            bar_width = 0.25
            index = np.arange(n_groups)
            zero_state_list = []
            one_state_list = []
            two_state_list = []
        

            for key in bin_states:
                zero_state_list.append(bin_states[key][0])
                one_state_list.append(bin_states[key][1]) 
                two_state_list.append(bin_states[key][2])

            
            

            rects1 = plt.bar(index, zero_state_list, bar_width,
                 alpha=opacity,
                 color='b',
                 label='state 0')

            rects2 = plt.bar(index + bar_width, one_state_list, bar_width,
                 alpha=opacity,
                 color='r',
                 label='state 1')

            rects3 = plt.bar(index + 2*bar_width, two_state_list, bar_width,
                 alpha=opacity,
                 color='g',
                 label='state 2')

            plt.xlabel('Bins')
            plt.ylabel('Count')
            plt.xticks(index + 2*bar_width / 2, data_bin)
            plt.legend()
            plt.title('State Distribution For File \''+length_file_clean+'\' with bin '+str(bin_number))
            plt.savefig('plots/length_state_distributions/'+length_file_clean+'_bin-'+str(bin_number)+'_distribution.png')
            #plt.tight_layout()
            plt.clf() # clear figure
            bin_number += 1
            
    



    return

def generate_probability_tables():
    # Generate nice looking emission and transion probability tables

    if(len(length_files) != len(state_files)):
        print("Need same number of states and lengths files")
        return

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

    colors = ['#DAF7A6','#FFC300','#FF5733','#C70039','#900C3F','#48C9B0','#A551CF','#16A085','#AEB6BF','#515A5A']

    if(len(length_files) < 2):
        print("Need to provide at least two sets of data, one for training and one for testing")
        return
    if(len(state_files) < 2):
        print("Need to provide at least two sets of data, one for training and one for testing")
        return
    if(len(length_files) != len(state_files)):
        print("Need same number of states and lengths files")
        return

    length = len(length_files)
    if length % 2 == 1:
        length -= 1
    
    for i in range(0,length,2):
        training_lengths_file = 'data/'+length_files[i]
        testing_lengths_file = 'data/'+length_files[i+1]
        training_states_file = 'data/'+state_files[i]
        testing_states_file = 'data/'+state_files[i+1]


        fig = plt.figure(1)
        ax = plt.gca()
        fig2 = plt.figure(2)
        ax2 = plt.gca()
        bin_number = 0
        # Run every bin on each file
        for data_bin in bins:
            training = hmm.do_train(training_lengths_file,training_states_file,data_bin)
            accuracy,f1_macro,f1_weighted = hmm.run_viterbi(testing_lengths_file,testing_states_file,training,data_bin)

            ax.scatter(len(data_bin),accuracy, c=colors[bin_number], label='bin '+str(bin_number))
            ax2.scatter(len(data_bin),f1_weighted, c=colors[bin_number], label='bin '+str(bin_number))

            bin_number += 1

        training_lengths = length_files[i][:-4]
        training_states = state_files[i][:-4]
        testing_lengths = length_files[i+1][:-4]
        testing_states = state_files[i+1][:-4]

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend()
        box = ax2.get_position()
        ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax2.legend()
        plt.figure(1)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.title('Bin Size vs. Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Bin Size')
        plt.savefig('plots/bin_accuracy/accuracy_train-'+training_lengths+'-'+training_states+'_test-'+testing_lengths+'-'+testing_states+'.png')
        plt.clf()
        plt.figure(2)
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.title('Bin Size vs. F-Measure')
        plt.ylabel('F-Meausre')
        plt.xlabel('Bin Size')
        plt.savefig('plots/bin_accuracy/fmeasure_train-'+training_lengths+'-'+training_states+'_test-'+testing_lengths+'-'+testing_states+'.png')
        #plt.show()
        plt.clf()
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

