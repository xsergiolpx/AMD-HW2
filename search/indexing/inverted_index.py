import json
import pprint
from collections import defaultdict, Counter
from search.download.manageFiles import saveToTSF

# TODO: Add fancy print

class InvertedIndex(object):

    def __init__(self, filename, types, debug=True):
        self.debug = debug
        if self.debug:
            self.pp = pprint.PrettyPrinter(indent=3)
        self.json = self.read_json(filename)
        self.tokens = []
        self.postings = defaultdict(list)
        self.types = types
        self.dictionary = {}

    def read_json(self, filename):
        """
        Load json file from generate_tokens.py
        :param filename: Name of the file containing all the tokens.
        :return: The json with the tokens.
        """
        with open(filename) as json_data:
            return json.load(json_data)

    def obtain_tokens(self):
        for doc in self.json:
            for type in self.types:
                try:
                    for i in self.json[doc][type]:
                        self.tokens.append((i, int(doc)))
                except TypeError:
                    continue

    def sort_tokens(self):
        self.tokens.sort(key=lambda x: (x[0], x[1]))

    def create_dictionary(self):
        # TODO: Decide what to do here.
        if len(self.postings) > 0:
            print("hola")
        else:
            print(self.postings.keys())

    def create_postings(self):
        for k, v in self.tokens:
            self.postings[k].append(v)

    def store_postings(self):
        for k, v in self.postings.items():
            if k == '':
                continue
            saveToTSF(map(str, v), "data/postings/"+ k)

    def get_postings(self):
        return self.postings
