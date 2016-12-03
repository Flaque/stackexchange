import toMySQL

def populateInMySQL():
    db = toMySQL.connect()
    print toMySQL.get_question_answers(db).fetchone()

    #toMySQL.update_similar_answer()

populateInMySQL()
