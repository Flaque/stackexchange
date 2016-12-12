import MySQLdb
import codecs

def insert_question(db, sitename, stackexchange_id, score, view_count,
    body):
    query = """
        INSERT INTO Questions
            SET site_id=(
                    SELECT id FROM Sites WHERE sitename=%s
                ),
                stackexchange_id=%s, score=%s, view_count=%s, body=%s
    """
    body = body.encode('utf-8')
    cursor = db.cursor()
    cursor.execute(query, (sitename, stackexchange_id, score, view_count,
        body))

def insert_answer(db, sitename, question_stackexchange_id, stackexchange_id,
    score, body):
    query = """
        INSERT INTO Answers
            SET question_id=(
                SELECT id FROM Questions WHERE stackexchange_id=%s
                AND site_id= (
                    SELECT id FROM Sites WHERE sitename=%s
                )
            ),
            stackexchange_id=%s, score=%s, body=%s

    """
    body = body.encode('utf-8')
    cursor = db.cursor()
    cursor.execute(query, (question_stackexchange_id, sitename,
        stackexchange_id, score, body))

def insert_site(db, name):
    query = 'INSERT INTO Sites (sitename) VALUES ("%s");' % (name)
    cursor = db.cursor()
    cursor.execute(query)

def bulk_insert_site(db, names):
    query = 'INSERT INTO Sites (sitename) VALUES (%s)'
    for i in range(1, len(names)):
        query += ' ,(%s)'

    cursor = db.cursor()
    cursor.execute(query, tuple(names))

def update_similar_answer(db, id, similarity):
    query = 'UPDATE Answers SET similarity="%s" WHERE id="%s"'
    db.query(query % (similarity, id))

def update_features(db, answer_id, valuesDict):
    query = """ UPDATE Answers SET
            similarity=%s,
            entities=%s,
            sentences=%s,
            link_ratio=%s,
            tag_ratio=%s
        WHERE id = %s
    """

    cursor = db.cursor()
    cursor.execute(query, (valuesDict['similarity'],
        valuesDict['entities'], valuesDict['sentences'],
        valuesDict['link_ratio'], valuesDict['tag_ratio'], answer_id))


def get_question_answers(db):
    query = """ SELECT Questions.id, Questions.body, Answers.id, Answers.body
        FROM Answers
        JOIN Questions ON Answers.question_id=Questions.id """

    cursor = db.cursor()
    cursor.execute(query)
    return cursor

def connect():
    return MySQLdb.connect(host='localhost', user='root', db='stackexchange')

def _test():
    db = connect()
    insert_site(db, 'testtwo')
    insert_question(db, 'testtwo', 1, 10, 100, 'hey there bro whats up?',
        0, 0, 0)
    insert_answer(db, 'testtwo', 1, 2, 10, 'not much man', 0,0,0)
    db.commit()
