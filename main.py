import xml_parse
import toMySQL

DATA_FOLDER = 'quick/'

def main():
    db = toMySQL.connect()
    xml_parse.populateSites(db, DATA_FOLDER)
    xml_parse.populateQuestions(db, DATA_FOLDER)
    xml_parse.populateAnswers(db, DATA_FOLDER)
    db.commit()

main()
