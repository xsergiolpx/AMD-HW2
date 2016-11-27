import os
def loadFromFile(filename):
    '''
    :param filename:
    :return:
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
    :param iterable: save this to the file
    :param filename:
    :return:
    '''
    with open(filename + '.txt', 'w') as f:
        f.write('\n'.join(iter))

def apendToFile(s, filename):
    with open(filename + ".txt", "a") as f:
        f.write(s)
        f.write("\n")


def saveToTSF(header, filename):
    '''
    :param header: save this to the file
    :param filename:
    :return:
    '''

    with open(filename + ".tsv", "a") as f:
        f.write("\t".join(header))
        f.write("\n")