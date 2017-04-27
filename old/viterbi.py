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

def dptable(V):
     # Print a table of steps from dictionary
     yield " ".join(("%12d" % i) for i in range(len(V)))
     for state in V[0]:
         yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)

if __name__ == "__main__":

    text_list = []
    #####################change file################################
    print "Parsing file... "
    with open ('penntree.tag', 'r') as sentences:
        text_list.append(("SSSS", "SSSS"))
        for line in sentences:
            if line == "\n":
                text_list.append(("EEEE", "EEEE"))
                text_list.append(("SSSS", "SSSS"))
            else:
                line_list = line.split()
                word = line_list[0]
                tag = line_list[1]
                text_list.append((word, tag))
                del line_list[:]
        text_list.append(("EEEE", "EEEE"))
    #print text_list
    print "Done parsing... "

    transition_prob = {}
    emission_prob = {}
    start_prob = {}
    tag_data = {}
    word_data = {}
    tag_count = {} #contains count of each tag
    tags = set()
    words = set()

    print "Storing occurences of tags in dictionary... "

    #Gets the number of each tags in file, stores them in dictionary. 
    for word, tag in text_list:     
        if tag not in tag_count.keys():
            tagCount = 0;
            for word1, tag1 in text_list:
                if tag == tag1:
                    tagCount +=1
                tag_count[tag] = tagCount

        tags.add(tag)
        words.add(word)

    #print tag_count['DT']

    print "Creating starting probabilities...  "

    for tag in tags:
        if tag == "SSSS":
            start_prob[tag] = 1
        else:
            start_prob[tag] = 0

    print "Creating dictionaries... "

    for tag in tags:
        if tag not in tag_data.keys():
            tag_data[tag] = {}
            transition_prob[tag] = {}
        for tag1 in tags:
            if tag1 not in tag_data[tag] and tag1 not in transition_prob[tag]: #if tag combination does not exist
                tag_data[tag][tag1] = 0
                transition_prob[tag][tag1] = 0

    for word in words:
        #if tag not in word_data.keys() and tag not in emission_prob.keys():
        word_data[word] = {}
        #emission_prob[tag] = {}
        for tag in tags:
          # if word not in word_data[word] and tag not in emission_prob[tag]:
            emission_prob[tag] = {}
            word_data[word][tag] = 0
            emission_prob[tag][word] = 0


    print "Appending values to dictionaries... "

    for word, tag in text_list:
        
        word_data[word][tag]+=1

    for x in range(0, len(text_list)):
        if x == len(text_list) -1:
            break
        first_tag = text_list[x][1]
        second_tag = text_list[x+1][1]
        tag_data[first_tag][second_tag] +=1

    #print word_data
    #print tag_data

    print "Storing emission and transition probabilities... "
            
    for tag in tags:
        for tag1 in tags:
            #if transition_prob[tag1][tag] == 0:
            transition_prob[tag1][tag] = float(tag_data[tag1][tag])/float(tag_count[tag]) 

    for word in words:
        for tag in tags:
            #if emission_prob[tag][word] == 0:
            emission_prob[tag][word] = float(word_data[word][tag])/float(tag_count[tag])

    print "Transition and emission probabilities calculated..."

    states = tags #SSSS and EEEE
    observations = ["SSSS", "Can", "a", "can", "can" ,"a", "can", "?", "EEEE"] #user-inputed strings
    start_probability = start_prob #Start probability for SSSS and EEEE are both 1
    transition_probability = transition_prob
    emission_probability = emission_prob
    viterbi(observations, states, start_probability, transition_probability, emission_probability)






