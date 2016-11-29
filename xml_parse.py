import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv
import os
from html_stats import stats
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

                    toMySQL.insert_question(db, sitename, stackexchange_id,
                        score, view_count, body)

        else:
            print 'ERROR: Posts.xml not found in', sitename



# def getParseTrees(data_folder, filename):
#     """ Gets all parse trees for all files named filename """
#     post_trees = []
#
#     # For every folder in `data`
#     for folder in os.listdir(data_folder):
#
#         # Avoid weird .DS_Store's on macs
#         if not os.path.isdir(DATA_FOLDER + folder):
#             continue
#
#         # Loop through each individual stack exchange folder to find `filename`
#         for foldername in os.listdir(data_folder + folder):
#             if foldername == POSTS_FILENAME:
#                 post_trees.append(ET.parse(data_folder + folder + '/'
#                     + filename))
#     return post_trees
#
# def soupify(body):
#     warnings.filterwarnings('error')
#
#     try:
#         return BeautifulSoup(body, 'html.parser')
#     except UserWarning: # Hides a `just a url` printout from BeautifulSoup
#         return BeautifulSoup(body, 'html.parser')
#
# def countCitations(body):
#     """ Returns the total citations (links) that are in the text """
#
#     warnings.filterwarnings('error')
#     try:
#         soup = BeautifulSoup(body, 'html.parser') #TODO: maybe move out? slowwww
#         return len(soup.find_all('a')) # Get all links
#     except UserWarning:
#         print 'Hey', body
#         return 1
#
# def main():
#     print("...Loading trees")
#     post_trees = getParseTrees(DATA_FOLDER, COMMENTS_FILENAME)


if __name__ == "__main__":
    #populateSites(DATA_FOLDER)
    populateQuestions(DATA_FOLDER)
