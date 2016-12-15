import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv
import os
import html_stats as stats
import warnings
import util
import toMySQL
import sys
import output

POST_TYPE = {
    'question' : 1,
    'answer'   : 2
}

POSTS_FILENAME = 'Posts.xml'

def populateSites(db, data_folder):

    folders = []
    count = 0
    for folder in os.listdir(data_folder):

        # Avoid weird .DS_store's on macs
        if not os.path.isdir(data_folder + folder):
            continue

        output.update("...Popluating site %s" % count)

        folders.append(folder)
        count+=1

    toMySQL.bulk_insert_site(db, folders)

def populateQuestions(db, data_folder):

    for sitename in os.listdir(data_folder):

        # Avoid weird .DS_store's on macs
        if not os.path.isdir(data_folder + sitename):
            continue

        if 'Posts.xml' in os.listdir(data_folder + sitename):
            tree = ET.parse(data_folder + sitename + '/Posts.xml')
            root = tree.getroot() #GROOT

            count = 0
            for post in root.iter('row'):
                if int(post.get('PostTypeId')) == POST_TYPE['question']:
                    stackexchange_id = post.get('Id')
                    score = post.get('Score')
                    view_count = post.get('ViewCount')
                    body = post.get('Body')


                    output.update("...Popluating question %s" % count)

                    toMySQL.insert_question(db, sitename, stackexchange_id,
                        score, view_count, body)
                    count += 1

        else:
            print 'ERROR: Posts.xml not found in', sitename

def populateAnswers(db, data_folder):

    for sitename in os.listdir(data_folder):

        # Avoid weird .DS_store's on macs
        if not os.path.isdir(data_folder + sitename):
            continue

        if 'Posts.xml' in os.listdir(data_folder + sitename):
            tree = ET.parse(data_folder + sitename + '/Posts.xml')
            root = tree.getroot() #GROOT

            count = 0
            for post in root.iter('row'):
                if int(post.get('PostTypeId')) == POST_TYPE['answer']:
                    stackexchange_id = post.get('Id')
                    score = post.get('Score')
                    question_id = post.get('ParentId')
                    body = post.get('Body')

                    output.update("...Popluating Answer %s" % count)
                    toMySQL.insert_answer(db, sitename, question_id,
                        stackexchange_id, score, body)
                    count +=1
        else:
            print 'ERROR: Posts.xml not found in', sitename
