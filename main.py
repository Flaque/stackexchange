import toMySQL
from knn import knn, normalize_table
from partition import holdout
from classifier_util import accuracy
from table_utils import discretize_column, getCol, discretize_table
import sys
import numpy
from numpy import mean, median, arange
from tabulate import tabulate
from visualization import genPlots
import time
from naive_bayes import naive_bayes
import os
import random_forest

SCORE_INDEX = 0
OUTPUT = 'output/'

def discretize_score(table, bins):
    table = discretize_column(table, SCORE_INDEX, bins)
    return table

def read():
    db = toMySQL.connect()
    table = [list(results) for results in toMySQL.get_answers(db)]
    db.commit()
    return table


def print_confusion_matrix(labels, class_label_name):
    """ Prints the confusion matrix of the given labels

    :param labels: A list of tuples of class labels [(actual, predicted),...]
    :param class_label_name: The name of the class label
    """
    class_labels = list(set(getCol(labels, 0)))  # all the actual class labels
    the_headers = [class_label_name]
    the_headers.extend(class_labels)
    the_headers.extend(['Total', 'Recognition (%)'])

    # makes an table filled with zeros of #columns = len(the_headers) and #rows = len(class_labels)
    confusion_matrix = [[0] * len(the_headers) for i in range(len(class_labels))]

    # fills out the confusion matrix with the predicted vs. actual
    for a_label_point in labels:
        actual, predicted = a_label_point
        confusion_matrix[class_labels.index(actual)][the_headers.index(predicted)] += 1

    # add the rest of the values to the confusion matrix
    for i in range(len(confusion_matrix)):
        row = confusion_matrix[i]  # current row

        # adding total to the confusion matrix
        total = sum(row)
        row[the_headers.index('Total')] = total  # add the total in for the row

        row[0]= class_labels[i]  # adds the class label for the row to the beginning of row

        # adding recognition to the confusion matrix (% of guesses in row that are correct
        recognition = row[the_headers.index(class_labels[i])] # TP
        recognition /= float(total)
        recognition *= 100
        row[the_headers.index('Recognition (%)')] = recognition

    # prints the table
    print tabulate(confusion_matrix, headers = the_headers, tablefmt="rst")

def summary(table):
    header = ["Attributes", "Min", "Max", "Mean", "Median"]
    attributes = ["Score", "Link Ratio", "Tag Ratio", "Entities", "Sentences",
        "Similarity"]
    summaryTable = [header]
    for i, att in enumerate(attributes):
        col = getCol(table, i)
        summaryTable.append([att, min(col), max(col), mean(col), median(col)])

    print tabulate(summaryTable, headers="firstrow", tablefmt="fancy")

def run_KNN(table, k):

    # Split table into training and test
    test, training = holdout(normalize_table(table, [0]))

    # Test accuracy of a knn
    labels = [(int(i), int(n)) for i, n in knn(training, test, k, SCORE_INDEX)]

    return labels

def test_KNN(table, maxK, maxBins):
    print "\n# Testing KNN"
    toTabulate = [["Attempt Number", "K", "Bins", "Accuracy", "Time in Seconds"]]

    # Test KNN for several variations of K.

    attempt = 1
    for bins in range(1, maxBins):

        # Discretize the scores
        discrete_table = discretize_score(table, bins=bins)

        # Run several variations of K
        for k in range(1, maxK):
            start = time.time()
            labels = run_KNN(discrete_table, k)
            acc = accuracy(labels)

            print "## Attempt Number", attempt
            print_confusion_matrix(labels, 'score')
            print '\n'
            toTabulate.append([k, bins, acc, str(time.time() - start) + "s"])
            attempt += 1

    print tabulate(toTabulate, headers="firstrow", tablefmt="simple")

def run_bayes(table):
    print "... Running Bayes"

    # Discretize the scores
    discrete_table = discretize_score(table, bins=6)

    test, training = holdout(normalize_table(table, [0]))

    labels = naive_bayes(test, training, SCORE_INDEX, (1, 2, 3, 4, 5))
    return labels

def test_bayes(table):
    print '\n# Testing Naive Bayes'

    start = time.time()
    labels = run_bayes(table)
    print "Time in Seconds:", str(time.time() - start) + "s"
    print_confusion_matrix(labels, 'score')
    print "\nAccuracy:", accuracy(labels)

def run_forest(table, N, M, F):
    indices = [1, 2, 3, 4, 5]
    labels, training, test = random_forest.run_a_table(table, indices, 0, N, M, F)
    return labels

def test_forest(table, maxN):
    print '\n# Testing Random Forest'

    toTabulate = [["Attempt Number", "N", "M", "F", "Accuracy", "Time in Seconds"]]
    attempt = 1

    for n in range(1, maxN):
        for m in range(1, n):
            for f in range(1, 4):

                start = time.time()
                labels = run_forest(table, n, m, f)
                toTabulate.append([attempt, n, m, f, accuracy(labels), \
                    str(time.time() - start) + 's'])
                attempt += 1

    print tabulate(toTabulate, headers="firstrow", tablefmt="fancy")

def main():

    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)

    # Record our output to an output.txt file
    original_stdout = sys.stdout
    f = file(OUTPUT + 'output' + str(time.time()) + '.txt', 'w')
    sys.stdout = f

    # Read table from MySQL
    table = read()

    # Generate summary data
    summary(table)
    #genPlots(table)

    test_forest(table, 1000)

    # Test a Naive Bayes Classifier
    #test_bayes(table)

    # Test a KNN Classifier
    #test_KNN(table, maxK=5, maxBins=15)

    # Close file and reset stdout
    sys.stdout = original_stdout
    f.close()

main()
