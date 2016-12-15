#import matplotlib.pyplot as plt
from table_utils import getCol
from tabulate import tabulate
from numpy import mean, median, arange
import os
import output


import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as pyplot

PDFs = 'pdfs/'

def genScatterPlot(filename, table, xIndex, yIndex, xLabel, yLabel, title):
    output.update("... Plot %s" % xLabel)
    pyplot.figure()

    ys = getCol(table, yIndex)
    xs = getCol(table, xIndex)

    pyplot.plot(xs, ys, 'b.', alpha=0.2)
    pyplot.xlabel(xLabel)
    pyplot.ylabel(yLabel)
    pyplot.suptitle(title)

    pyplot.savefig(PDFs + filename)

def genFrequencyGraph(filename, table, index, label, title):
    output.update("... Plot %s" % label)

    pyplot.figure()
    xs = getCol(table, index)
    pyplot.hist(xs, bins=100)
    pyplot.suptitle(title)
    pyplot.xlabel(label)

    pyplot.savefig(PDFs + filename)

def genPlots(table):
    if not os.path.exists(PDFs):
        os.makedirs(PDFs)

    genScatterPlot('dot-score-links.pdf', table, 1, 0, 'Link Ratio', 'Score',
        'Link Ratio vs Score')
    genScatterPlot('dot-score-tag.pdf', table, 2, 0, 'Tag Ratio', 'Score',
        'Tag Ratio vs Score')
    genScatterPlot('dot-score-entities.pdf', table, 3, 0, 'Entities', 'Score',
        'Entities vs Score')
    genScatterPlot('dot-score-sentences.pdf', table, 4, 0, 'Sentences', 'Score',
        'Sentences vs Score')
    genScatterPlot('dot-score-sim.pdf', table, 5, 0, 'Similarity', 'Score',
        'Similarity vs Score')

    genFrequencyGraph('freq-score.pdf', table, 0, 'Score', 'Score')
    genFrequencyGraph('freq-links.pdf', table, 1, 'Link Ratio', 'Link Ratio')
    genFrequencyGraph('freq-tags.pdf', table, 2, 'Tag Ratio', 'Tag Ratio')
    genFrequencyGraph('freq-ents.pdf', table, 3, 'Entities', 'Entites')
    genFrequencyGraph('freq-sents.pdf', table, 4, 'Sentences', 'Sentences')
