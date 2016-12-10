import pprint
from collections import defaultdict, Counter
from search.download.manageFiles import save_to_tsv, read_json, write_json, read_from_tsv
from collections import deque, Counter
from itertools import dropwhile
from math import sqrt, log10

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
        self.term_frequencies = {}
        self.length = {}

    def obtain_tokens(self):
        self.json = read_json(self.filename)

        if self.debug:
            n = len(self.json)
            print(n)
            j=0

        for doc in self.json:
            if self.debug:
                j+=1
                if j%50==0:
                    print("[tokens] %0.2f%s"%(j/n*100.0,'%'))

            for type in self.types:
                try:
                    for i in self.json[doc][type]:
                        if i == '':
                            continue
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

        lengths = {}

        for k, v in self.tokens:
            if k == '':
                continue
            idx = self.dictionary.get(k)
            if idx is None:
                lengths[k] = 1
                self.dictionary[k] = {'n': 1,
                                      'posting': "data/postings/" + k,
                                      'term_frequency': "data/term_frequencies/" + k }
            else:
                lengths[k] += 1
                self.dictionary[k]["n"] += 1
            self.postings[k].append(v)

        with open("data/documents.csv", 'r') as file_n:
            n = int(file_n.readline())

        for k in self.postings.keys():
            self.postings[k].insert(0, n*1.0/lengths[k])

    @staticmethod
    def load_frequencies(filename):
        return read_from_tsv(filename, lines=True)

    def store_postings(self):
        for k, v in self.postings.items():
            if k == '':
                continue
            save_to_tsv(map(str, v), "data/postings/" + k)

    @staticmethod
    def load_posting(posting):
        with open(posting + ".tsv", "r") as f:
            list_str = list(map(str, f.readline().split('\t')))
            n_dft = float(list_str[0])
            postings = list(map(int, list_str[1:]))

            return [n_dft]+postings

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
                union_dict[name] = self.union(map(lambda x: self.load_posting(self.dictionary[x]["posting"])[1:],
                                                  k_near.split()))
                to_sort[name] = len(union_dict[name])

        times = 0

        for k, _ in sorted(to_sort.items(), key=lambda x: x[1]):
            if times == 0:
                times += 1
                try:
                    answer = deque(self.load_posting(self.dictionary[k]["posting"])[1:])
                except KeyError:
                    answer = deque(union_dict[k])
            else:
                try:
                    answer = self.intersection(answer, deque(self.load_posting(self.dictionary[k]["posting"])[1:]))
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
        d, N, M = dict(), len(str1), len(str2)
        for i in range(N + 1):
            d[i] = dict()
            d[i][0] = i
        for i in range(M + 1):
            d[0][i] = i
        for i in range(1, N + 1):
            for j in range(1, M + 1):
                d[i][j] = min(d[i][j - 1] + 1, d[i - 1][j] + 1, d[i - 1][j - 1] + (not str1[i - 1] == str2[j - 1]))
        return d[N][M]

    def k_near_string(self, string, k, type="near"):
        """
        Calculates either the k nearest neighbors to string or the neighbors with distance at most k from string.
        :param string: The string we want to find relatives.
        :param k: The parameter k.
        :param type: The type of k_near we want.
        :return: The list depending on type.
        """
        distances = Counter()
        for doc in self.dictionary.keys():
            if doc == '':
                continue
            if doc[0] == string[0]:
                distances[doc] = self.distance(string, doc)

        if type == "tolerance":
            # Return n elements with tolerance at most k
            for k, c in dropwhile(lambda c: c[1] <= k, reversed(distances.most_common())):
                del distances[k]
            return distances.most_common()
        elif type == "near":
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

    def load_norm(self):
        with open("data/length.tsv", 'r') as length_file:
            for line in length_file:
                docid, norm = line.split("\t")
                self.length[int(docid)] = float(norm)

    def cosine_score(self, q):
        # Get the terms of the query
        query = q.split()

        # Get posting list given query
        documents = self.intersection_list(query, 5)

        # Initialize scores
        scores = {}
        for d in documents:
            scores[d] = 0

        # Spell correction
        terms = []
        for term in query:
            exist = self.dictionary.get(term)
            if exist is None:
                union = [k for k, v in self.k_near_string(term, 5)]
                terms += union
            else:
                terms += [term]

        # Calculate w_t,q
        wt_q = 1.0/sqrt(len(terms))

        for term in terms:
            tf_td = self.load_frequencies(self.dictionary[term]["term_frequency"])
            posting_t = self.load_posting(self.dictionary[term]["posting"])
            wft_d = log10(posting_t[0])
            for doc in documents:
                try:
                    tf_idf_t_d = tf_td[doc] * wft_d
                except KeyError:
                    tf_idf_t_d = wft_d
                scores[doc] += wt_q * tf_idf_t_d

        self.load_norm()
        # normalize
        for doc in documents:
            scores[doc] /= self.length[doc]

        return reversed(sorted(scores.items(), key=lambda x: x[1]))