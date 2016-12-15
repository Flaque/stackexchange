import xml_parse
import toMySQL
import features
import sys

DATA_FOLDER = 'quick/'

def firstPass():
    """ Populates the questions and answers and adds their content """
    print "## Attempting to populate the question and answer content."
    db = toMySQL.connect()
    xml_parse.populateSites(db, DATA_FOLDER)
    db.commit()
    xml_parse.populateQuestions(db, DATA_FOLDER)
    db.commit()
    xml_parse.populateAnswers(db, DATA_FOLDER)
    db.commit()

def secondPass():
    """ Populates the questions and answers with features """

    print "## Attempting to populate the features for the question and answers."
    db = toMySQL.connect()
    count = 0
    for _, question, answer_id, answer in toMySQL.get_question_answers(db):
        valuesDict = features.answer(question, answer)
        toMySQL.update_features(db, answer_id, valuesDict)

        # Update log
        sys.stdout.write('\r ...Computing %s answers' % count)
        sys.stdout.flush()
        count += 1
    db.commit()

def populate():
    print "# Attempting to populate the database"
    firstPass()
    secondPass()

populate()
