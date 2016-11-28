import _mysql

def insert_question(db, sitename, stackexchange_id, score, view_count, body):
    query = """
        INSERT INTO Questions
            SET site_id=(
                    SELECT id FROM Sites WHERE sitename='%s'
                ),
                stackexchange_id='%s', score='%s', view_count='%s', body='%s'
    """
    db.query(query % (sitename, stackexchange_id, score, view_count, body))

def insert_answer(db, question_id):
    pass

def insert_site(db, name):
    query = 'INSERT INTO Sites (sitename) VALUES ("%s");' % (name)
    db.query(query)

def connect():
    return _mysql.connect(host='localhost', user='root', db='stackexchange')

def main():
    db = connect()
    insert_site(db, 'testtwo')
    insert_question(db, 'testtwo', 1, 10, 100, 'hey there bro whats up?')

main()
