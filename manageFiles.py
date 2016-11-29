import os
def loadFromFile(filename):
    '''
    Loads filename. If it does not exist, it is created.
    :param filename: filename to load without extension
    :return: list in which each element has one line of filename.txt
    '''
    if os.path.exists(filename + ".txt"):
        with open(filename + ".txt", "r+") as f:
            array = []
            for line in f:
                array.append(line.strip('\n'))
    else:
        with open(filename + ".txt", "w+") as f:
            array = []
            for line in f:
                array.append(line.strip('\n'))
    return array

def saveToFile(iter, filename):
    '''
    :param iterable: save this iterable to the file. Each element in a new line
    :param filename: filename
    :return: nothing
    '''
    with open(filename + '.txt', 'w') as f:
        f.write('\n'.join(iter))

def apendToFile(s, filename):
    '''
    appends to a new line the string s to the file filename.txt
    :param s: this is a string
    :param filename: filename of the file
    :return: nothing
    '''
    with open(filename + ".txt", "a") as f:
        f.write(s)
        f.write("\n")


def saveToTSF(header, filename):
    '''
    Apends the list "header" to the file filename.txt.
    This is a tsv, so each element of the list is
    separated by a tab in the file
    :param header: list of elements
    :param filename: name of the file
    :return: nothing
    '''

    with open(filename + ".tsv", "a") as f:
        f.write("\t".join(header))
        f.write("\n")
