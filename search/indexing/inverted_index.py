import pprint
from collections import defaultdict, Counter
from search.download.manageFiles import save_to_tsv, read_json, write_json, read_from_tsv
from collections import deque, Counter
from itertools import dropwhile
# TODO: Add fancy print
# TODO: Change filename to: tokens_file, dictionary_file


class InvertedIndex(object):

    def __init__(self, name, filename, types, debug=True):
        self.debug = debug
        if self.debug:
            self.pp = pprint.PrettyPrinter(indent=3)
        self.name = name
        self.filename = filename
        self.json = None
        self.tokens = []
        self.postings = defaultdict(list)
        self.types = types
        self.dictionary = {}

    def obtain_tokens(self):
        self.json = read_json(self.filename)

        if self.debug:
            n = len(self.json)
            j=0

        for doc in self.json:
            if self.debug:
                j+=1
                if j%50==0:
                    print("[tokens] %0.2f%s"%(j/n*100.0,'%'))

            for type in self.types:
                try:
                    for i in self.json[doc][type]:
                        self.tokens.append((i, int(doc)))
                except TypeError:
                    continue
        # (i, int(doc)) could be in 2 types
        self.tokens = list(set(self.tokens))

    def sort_tokens(self):
        if self.debug:
            print("[sorting] Tokens")

        self.tokens.sort(key=lambda x: (x[0], x[1]))

    def create_dictionary(self):
        for k, v in self.tokens:
            idx = self.dictionary.get(k)
            if idx is None:
                self.dictionary[k] = {'n': 1,
                                      'posting': "data/postings/" + k}
            else:
                self.dictionary[k]['n'] += 1
            self.postings[k].append(v)

    def store_postings(self):
        for k, v in self.postings.items():
            if k == '':
                continue
            save_to_tsv(map(str, v), "data/postings/" + k)

    @staticmethod
    def retrieve_posting(posting):
        return read_from_tsv(posting)

    @staticmethod
    def intersection(p1, p2):
        """
        Implementation of algorithm in figure 1.6 Information Retrieval p.11
        :param p1: First deque of docid terms.
        :param p2: Second deque of docid terms.
        :return: The intersection between docid deques p1 and p2.
        """
        answer = deque()
        while len(p1) != 0 and len(p2) != 0:
            d1, d2 = p1.popleft(), p2.popleft()
            if d1 == d2:
                answer.append(d1)
            elif d1 < d2:
                p2.appendleft(d2)
            else:
                p1.appendleft(d1)
        return answer

    def intersection_list(self, names, k, type="tolerance"):
        """
        Implementation of algorithm in figure 1.7, Information Retrieval, p.12
        Remark: If name[i] isn't in postings then we create Union of terms near name[i].
        :param names: List of tokens to intersect
        :param k: Parameter to k_near_string which can mean: at least k occurrences or k most similar.
        :param type: Type of method k_near_string.
        :return: The intersection between terms inside names.
        """
        # create dict
        to_sort = dict()
        union_dict = dict()
        answer = deque()

        for name in names:
            try:
                to_sort[name] = self.dictionary[name]["n"]
            except KeyError:
                # Create names of k near strings to name
                k_near = " ".join(k for k, v in self.k_near_string(name, k, type))
                union_dict[name] = self.union(map(lambda x: self.retrieve_posting(self.dictionary[x]["posting"]),
                                                  k_near.split()))
                to_sort[name] = len(union_dict[name])

        times = 0

        for k, _ in sorted(to_sort.items(), key=lambda x: x[1]):
            if times == 0:
                times += 1
                try:
                    answer = deque(self.retrieve_posting(self.dictionary[k]["posting"]))
                except KeyError:
                    answer = deque(union_dict[k])
            else:
                try:
                    answer = self.intersection(answer, deque(self.retrieve_posting(self.dictionary[k]["posting"])))
                except KeyError:
                    answer = self.intersection(answer, deque(union_dict[k]))

        return list(answer)

    @staticmethod
    def intersection_array(p1, p2):
        answer = []
        while p1 != [] and p2 != []:
            d1, d2 = p1[0], p2[0]
            if d1 == d2:
                answer.append(d1)
                p1, p2 = p1[1:], p2[1:]
            else:
                if d1 < d2:
                    p1 = p1[1:]
                else:
                    p2 = p2[1:]
        return answer

    @staticmethod
    def distance(str1, str2):
        """
        https://web.stanford.edu/class/cs124/lec/med.pdf
        :param str1:
        :param str2:
        :return:
        """
        d = dict()
        for i in range(len(str1) + 1):
            d[i] = dict()
            d[i][0] = i
        for i in range(len(str2) + 1):
            d[0][i] = i
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                d[i][j] = min(d[i][j - 1] + 1, d[i - 1][j] + 1, d[i - 1][j - 1] + (not str1[i - 1] == str2[j - 1]))
        return d[len(str1)][len(str2)]

    def k_near_string(self, string, k, type="tolerance"):
        """
        Calculates either the k nearest neighbors to string or the neighbors with distance at most k from string.
        :param string: The string we want to find relatives.
        :param k: The parameter k.
        :param type: The type of k_near we want.
        :return: The list depending on type.
        """
        distances = Counter()
        for doc in self.dictionary.keys():
            if doc[0] == string[0]:
                distances[doc] = self.distance(string, doc)

        if type == "tolerance":
            # Return n elements with tolerance at most k
            for k, c in dropwhile(lambda c: c[1] <= k, reversed(distances.most_common())):
                del distances[k]

            return distances.most_common()
        else:
            # Return k elements with the lowest score
            return distances.most_common()[:-k - 1:-1]

    def union(self, mp):
        """
        Creates the sorted union list inside every element of generator mp.
        :param mp: The generator that contains all the lists.
        :return: The sorted union list.
        """
        union = set()
        for l in mp:
            union = union | set(l)
        return sorted(list(union))

    def store_dictionary(self):
        """
        Store the dictionary in a json file.
        """
        write_json('data/dictionaries/' + self.name + '.json', self.dictionary)

    def load_dictionary(self, filename):
        """
        Loads the dictionary in file filename.
        :param filename: The name of the file.
        """
        self.dictionary = read_json(filename)

    def get_postings(self):
        """
        Retrieves the postings entirely
        :return: The postings structure.
        """
        return self.postings

    def get_dictionary(self):
        return self.dictionary
