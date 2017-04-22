# made this file in case anyone else is working on something to avoid merge conflicts

from sklearn.metrics import f1_score, classification_report, confusion_matrix

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

calculate_metrics([0,0,0,0,0,0,1,2,3],[0,1,0,3,0,0,1,2,3])
calculate_metrics([0,0,0],[0,1,0,3,0,0,1,2,3])
calculate_metrics([0,1,0,3,0,0,1,2,3],[0,1,0,3,0,0,1,2,3])
calculate_metrics([1,2,3,1,2,3,1,2,3],[1,2,3,1,2,3,1,2,3])
