import os
import json
# TODO: PEP names


def load_from_file(filename):
    """
    Loads filename. If it does not exist, it is created.
    :param filename: filename to load without extension
    :return: list in which each element has one line of filename.txt
    """
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


def save_to_file(iter, filename):
    """
    :param iterable: save this iterable to the file. Each element in a new line
    :param filename: filename
    :return: nothing
    """
    with open(filename + '.txt', 'w') as f:
        f.write('\n'.join(iter))


def append_to_file(s, filename):
    """
    appends to a new line the string s to the file filename.txt
    :param s: this is a string
    :param filename: filename of the file
    :return: nothing
    """
    with open(filename + ".txt", "a") as f:
        f.write(s)
        f.write("\n")


def save_to_tsv(header, filename):
    """
    Apends the list "header" to the file filename.txt.
    This is a tsv, so each element of the list is
    separated by a tab in the file
    :param header: list of elements
    :param filename: name of the file
    :return: nothing
    """
    with open(filename + ".tsv", "a") as f:
        f.write("\t".join(header))
        f.write("\n")


def read_from_tsv(filename, lines=False):
    try:
        if not lines:
            with open(filename + ".tsv", "r") as f:
                return list(map(int, f.readline().split('\t')))
        else:
            structure = {}
            with open(filename + ".tsv", "r") as f:
                for line in f:
                    k, v = line.split('\t')
                    structure[int(k)] = int(v)
                return structure
    except FileNotFoundError:
        return []


def read_json(filename):
    """
    Load json file.
    :param filename: Path to the json file.
    :return: The json with the data.
    """
    with open(filename) as json_data:
        return json.load(json_data)


def write_json(filename, data):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file)

def delete_file(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
