import itertools

def _validRow(row, where):
    """ Returns True if row matches where

    - where is a 2d array of index, value tuples
        ex: [(0, 'cats'), (1, 230)]
    """
    for index, value in where:
        if row[index] != value:
            return False

    return True

def getWhere(table, where):
    """ Gets rows that match the points defined in "where"
    ex: getWhere(table, [(1, 'dogs'), (0, 20)]))

    - where is a 2d array of index, value tuples
        ex: [(0, 'cats'), (1, 230)]
        note: These are AND'd together.
    """

    newTable = []
    for row in table:
        if _validRow(row, where):
            newTable.append(row)
    return newTable

def getCol(table, index):
    """ Gets a col by an index
    Ignores "NA"
    """
    col = []
    for row in table:
        if (row[index] == 'NA'): continue
        col.append(row[index])
    return col

def mapCol(table, colIndex, function):
    """ Applys the function to every item in the column """
    for row in table:
        row[colIndex] = function(row[colIndex])
    return table


def get_domains(table, att_indexes):
    """ Based on a table gets the domains for the given att_indexes

    :param table: a table
    :param att_indexes: list of indexes to get domains for
    :return: a dictionary {att:domain, ...}
    """
    domains = {}
    for index in att_indexes:
        att_vals = list(set(getCol(table, index)))
        domains[index] = att_vals
    return domains

def _cutoffs(table, col_index, num_bins):
    """ Returns a number of equal width cutoff points """
    col = getCol(table, col_index)
    min_val = min(col)
    max_val = max(col)
    width   = int(max_val - min_val) / num_bins
    return list(range(min_val + width, max_val + 1, width))

def _bin(array, splits):
    bins = []
    for split in splits:
        bins.append(array[:array.index(split)])
        array[:array.index(split)] = [] #remove that section of array
    if array:
        bins.append(array)
    return bins

def bin_table_col(table, col_index, num_bins):
    cuts = _cutoffs(table, col_index, num_bins)
    tableSorted = table.sort(key=lambda x: x[col_index])



if __name__ == "__main__":
    print _bin([1,2,3,4,5], [2, 4])
