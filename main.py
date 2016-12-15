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
import logging
import output

SCORE_INDEX = 0
OUTPUT = 'output/'

def discretize_score(table, bins):
    table = discretize_column(table, SCORE_INDEX, bins)
    return table

def read(limit):
    db = toMySQL.connect()
    table = [list(results) for results in toMySQL.get_answers(db, limit)]
    db.commit()
    return table


def confusion_matrix(labels, class_label_name):
    """ Prints the confusion matrix of the given labels

    :param labels: A list of tuples of class labels [(actual, predicted),...]
    :param class_label_name: The name of the class label
    """
    class_labels = list(set(getCol(labels, 0)))  # all the actual class labels
    the_headers = [class_label_name]
    the_headers.extend(class_labels)
    the_headers.extend(['Total', 'Recognition (%)'])

    # makes an table filled with zeros of #columns = len(the_headers) and #rows = len(class_labels)
    _confusion_matrix = [[0] * len(the_headers) for i in range(len(class_labels))]

    # fills out the confusion matrix with the predicted vs. actual
    for a_label_point in labels:
        actual, predicted = a_label_point
        _confusion_matrix[class_labels.index(actual)][the_headers.index(predicted)] += 1

    # add the rest of the values to the confusion matrix
    for i in range(len(_confusion_matrix)):
        row = _confusion_matrix[i]  # current row

        # adding total to the confusion matrix
        total = sum(row)
        row[the_headers.index('Total')] = total  # add the total in for the row

        row[0]= class_labels[i]  # adds the class label for the row to the beginning of row

        # adding recognition to the confusion matrix (% of guesses in row that are correct
        recognition = row[the_headers.index(class_labels[i])] # TP
        recognition /= float(total)
        recognition *= 100
        row[the_headers.index('Recognition (%)')] = recognition

    logging.info('\n' + str(tabulate(_confusion_matrix, headers = the_headers, tablefmt="rst")))

def summary(table):
    header = ["Attributes", "Min", "Max", "Mean", "Median"]
    attributes = ["Score", "Link Ratio", "Tag Ratio", "Entities", "Sentences",
        "Similarity"]
    summaryTable = [header]
    for i, att in enumerate(attributes):
        col = getCol(table, i)
        summaryTable.append([att, min(col), max(col), mean(col), median(col)])

    logging.info('\n' + str(tabulate(summaryTable, headers="firstrow", tablefmt="fancy")))

def run_KNN(table, k):

    # Split table into training and test
    test, training = holdout(normalize_table(table, [0]))

    # Test accuracy of a knn
    labels = [(int(i), int(n)) for i, n in knn(training, test, k, SCORE_INDEX)]

    return labels

def test_KNN(table, k):

    # Test KNN for several variations of K.
    output.update("... Testing KNN")
    logging.info("KNN report")
    start = time.time()
    labels = run_KNN(table, k)
    confusion_matrix(labels, 'score')
    logging.info('KNN at k=%s has %s accuracy in %s seconds' %
        (k, accuracy(labels), str(time.time() - start)))

def run_bayes(table):
    logging.info("... Running Bayes")

    test, training = holdout(normalize_table(table, [0]))

    labels = naive_bayes(test, training, SCORE_INDEX, (1, 2, 3, 4, 5))
    return labels

def test_bayes(table):
    logging.info('\n# Testing Naive Bayes')

    discrete_table = discretize_table(table, [(1, 10), (2, 10), (3, 10), (4, 10), (5, 10)])

    start = time.time()
    labels = run_bayes(discrete_table)
    output.update("... Running Naive Bayes")
    logging.info("Time in Seconds:" + str(time.time() - start) + "s")
    confusion_matrix(labels, 'score')
    logging.info("\nAccuracy:" + str(accuracy(labels)))

def run_forest(table, N, M, F):
    indices = [1, 2, 3, 4, 5]
    labels, training, test = random_forest.run_a_table(table, indices, 0, N, M, F)
    return labels

def test_forest(table, maxN):
    logging.info('\n# Testing Random Forest')

    toTabulate = [["Attempt Number", "N", "M", "F", "Accuracy", "Time in Seconds"]]
    attempt = 1

    for n in range(1, maxN):
        output.update("... Running Trees for n=%s" % n)
        for m in range(1, n):
            for f in range(1, 4):
                start = time.time()
                labels = run_forest(table, n, m, f)
                toTabulate.append([attempt, n, m, f, accuracy(labels), \
                    str(time.time() - start) + 's'])
                attempt += 1

    logging.info('\n' + str(tabulate(toTabulate, headers="firstrow", tablefmt="fancy")))

def main(arg):

    # Create log file
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    logging.basicConfig(filename=OUTPUT + 'output-' + str(time.time()) + '.txt', level=logging.INFO)

    # Read table from MySQL
    table = read(arg)

    # Generate summary data
    summary(table)
    genPlots(table)

    table = discretize_score(table, bins=3)

    # Test a KNN Classifier
    test_KNN(table, 5)

    # Test a Naive Bayes Classifier
    test_bayes(table)

    # Test forest
    test_forest(table, 10)

    output.update(" " * 20)
    output.update("---> Finished.")

if __name__ == "__main__":

    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main(800)
