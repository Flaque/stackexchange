import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv
import os
import html_stats as stats
import warnings
import util
import toMySQL

POST_TYPE = {
    'question' : 1,
    'answer'   : 2
}

DATA_FOLDER = 'quick/'
POSTS_FILENAME = 'Posts.xml'

def populateSites(data_folder):

    folders = []
    for folder in os.listdir(data_folder):

        # Avoid weird .DS_store's on macs
        if not os.path.isdir(data_folder + folder):
            continue

        folders.append(folder)

    db = toMySQL.connect()
    toMySQL.bulk_insert_site(db, folders)

def populateQuestions(data_folder):

    db = toMySQL.connect()

    for sitename in os.listdir(data_folder):

        # Avoid weird .DS_store's on macs
        if not os.path.isdir(data_folder + sitename):
            continue

        if 'Posts.xml' in os.listdir(data_folder + sitename):
            tree = ET.parse(data_folder + sitename + '/Posts.xml')
            root = tree.getroot() #GROOT

            for post in root.iter('row'):
                if int(post.get('PostTypeId')) == POST_TYPE['question']:
                    stackexchange_id = post.get('Id')
                    score = post.get('Score')
                    view_count = post.get('ViewCount')
                    body = post.get('Body')
                    links = stats.links(body)
                    tags = stats.tags(body)
                    word_count = stats.word_count(body)

                    toMySQL.insert_question(db, sitename, stackexchange_id,
                        score, view_count, body, links, tags, word_count)

        else:
            print 'ERROR: Posts.xml not found in', sitename

def populateAnswers(data_folder):

    db = toMySQL.connect()

    for sitename in os.listdir(data_folder):

        # Avoid weird .DS_store's on macs
        if not os.path.isdir(data_folder + sitename):
            continue

        if 'Posts.xml' in os.listdir(data_folder + sitename):
            tree = ET.parse(data_folder + sitename + '/Posts.xml')
            root = tree.getroot() #GROOT

            for post in root.iter('row'):
                if int(post.get('PostTypeId')) == POST_TYPE['answer']:
                    stackexchange_id = post.get('Id')
                    score = post.get('Score')
                    question_id = post.get('ParentId')
                    body = post.get('Body')

                    links = stats.links(body)
                    tags = stats.tags(body)
                    word_count = stats.word_count(body)

                    toMySQL.insert_answer(db, sitename, question_id,
                        stackexchange_id, score, body, tags, links, word_count)
        else:
            print 'ERROR: Posts.xml not found in', sitename

if __name__ == "__main__":
    populateSites(DATA_FOLDER)
    populateQuestions(DATA_FOLDER)
    populateAnswers(DATA_FOLDER)
