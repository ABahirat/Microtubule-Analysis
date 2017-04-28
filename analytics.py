import matplotlib.pyplot as plt

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
    plt.savefig('plots/'+state_file+'_distrobution.png')
    plt.clf() # clear figure


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
        plt.savefig('plots/'+length_file_clean+'_bin-'+str(bin_number)+'_distrobution.png')
        plt.clf() # clear figure

        bin_number += 1
