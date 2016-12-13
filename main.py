import toMySQL
from knn import knn, normalize_table
from partition import holdout
from classifier_util import accuracy
import sys

def read():
    db = toMySQL.connect()
    table = [list(results) for results in toMySQL.get_answers(db)]
    db.commit()

    return table

def main():

    # Read table from MySQL
    table = read()

    # Split table into training and test
    test, training = holdout(normalize_table(table, [0]))

    # Test accuracy of a knn
    labels = [(int(i), int(n)) for i, n in knn(training, test, 5, 0)]
    print accuracy(labels)
    print labels

main()
