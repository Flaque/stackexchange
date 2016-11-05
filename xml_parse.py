import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv
import os
from html_stats import stats

DATA_FOLDER = 'data/'
POSTS_FILENAME = 'Posts.xml'
COMMENTS_FILENAME = 'Comments.xml'
HEADER = ['Score', 'Characters', 'Citations', 'Total Tags']

def getParseTrees(data_folder, filename):
    """ Gets all parse trees for all files named filename """
    post_trees = []

    # For every folder in `data`
    for folder in os.listdir(data_folder):

        # Avoid weird .DS_Store's on macs
        if not os.path.isdir(DATA_FOLDER + folder):
            continue

        # Loop through each individual stack exchange folder to find `filename`
        for foldername in os.listdir(data_folder + folder):
            if foldername == POSTS_FILENAME:
                post_trees.append(ET.parse(data_folder + folder + '/'
                    + filename))
    return post_trees


print("...Loading trees")
post_trees = getParseTrees(DATA_FOLDER, COMMENTS_FILENAME)

print("Created all trees")

total = 0

with open('data.csv', 'wb') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(HEADER)

    for tree in post_trees:
        root = tree.getroot()
        for row in root.iter('row'):
            total += 1 # count totals

            # Count characters
            body = row.get('Text')
            characters = len(body)

            # Count votes
            score = row.get('Score')

            # Count citations
            soup = BeautifulSoup(body, 'html.parser')
            citations = len(soup.find_all('a')) # Get all links

            total_tags = stats(body)

            # Write to csv
            csv_writer.writerow([score, characters, citations, total_tags])
