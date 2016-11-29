import _mysql
import codecs

def insert_question(db, sitename, stackexchange_id, score, view_count,
    body, links, tags, word_count):
    query = """
        INSERT INTO Questions
            SET site_id=(
                    SELECT id FROM Sites WHERE sitename='%s'
                ),
                stackexchange_id='%s', score='%s', view_count='%s', body='%s',
                links='%s', tags='%s', words='%s'
    """
    body = body.encode('utf-8')
    db.query(query % (sitename, stackexchange_id, score, view_count,
    _mysql.escape_string(body), links, tags, word_count))

def insert_answer(db, sitename, question_stackexchange_id, stackexchange_id, score, body):
    query = """
        INSERT INTO Answers
            SET question_id=(
                SELECT id FROM Questions WHERE stackexchange_id='%s'
                AND site_id= (
                    SELECT id FROM Sites WHERE sitename='%s'
                )
            ),
            stackexchange_id='%s', score='%s', body='%s'
    """
    body = body.encode('utf-8')
    filled_query = query % (question_stackexchange_id, sitename,
        stackexchange_id, score, _mysql.escape_string(body))

    db.query(filled_query)

def insert_site(db, name):
    query = 'INSERT INTO Sites (sitename) VALUES ("%s");' % (name)
    db.query(query)

def bulk_insert_site(db, names):
    query = 'INSERT INTO Sites (sitename) VALUES ("%s")'
    for i in range(1, len(names)):
        query += ' ,("%s")'

    db.query(query % tuple(names))

def connect():
    return _mysql.connect(host='localhost', user='root', db='stackexchange')

def _main():
    db = connect()
    #insert_site(db, 'testtwo')
    #insert_question(db, 'testtwo', 1, 10, 100, 'hey there bro whats up?')
    #insert_answer(db, 'testtwo', 1, 2, 10, 'not much man')


_main()
