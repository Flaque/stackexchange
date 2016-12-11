import toMySQL
import lsa
import pprint

def populateInMySQL():
    db = toMySQL.connect()
    sims = {}
    for _, question, answer_id, answer in toMySQL.get_question_answers(db):
        sims[answer_id] = lsa.sim(question, answer)

    for answer_id, sim in sims.iteritems():
        toMySQL.update_similar_answer(db, answer_id, sim)

    db.commit()

populateInMySQL()
