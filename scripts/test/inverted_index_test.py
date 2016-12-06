from search.indexing.inverted_index import InvertedIndex
from search.preprocess.data_processing import generate_json, tokenize_CSV
import argparse

# TODO: Find out how to pass a vector to argparse for types


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', 
                        help='Filename of the tokens. It should be in data.',
                        dest="filename", 
                        required=True)
    parser.add_argument('-n', '--name',
                        help='Filename of Output dictionary.',
                        dest="name",
                        required=True)
    parser.add_argument('-s', '--store',
                        help="Do we store postings and dictionaries?",
                        action="store_true",
                        dest="store")
    parser.add_argument('-p', '--preprocess',
                        help="Use preprocessing to create tokens.json?",
                        action="store_true",
                        dest="preprocess")
    parser.add_argument('-d', '--debug',
                        help="Debug is passed.",
                        action="store_true",
                        dest="debug")
    arguments = parser.parse_args()
    
    return arguments, parser


def main():
    args, parser = get_args()

    if args.preprocess:
        generate_json(tokenize_CSV())

    inverted = InvertedIndex(name=args.name,
                             filename=args.filename,
                             types=['author', 'ingredients', 'method', 'programme', 'recipe_name'],
                             debug=args.debug)

    inverted.obtain_tokens()
    inverted.sort_tokens()
    inverted.create_dictionary()

    if args.store:
        inverted.store_postings()
        inverted.store_dictionary()

    postings = inverted.get_postings()

    i = 0

    for k, v in postings.items():
        if i < 200:
            print(k, v)
            print(inverted.retrieve_posting('data/postings/' + k))
            i += 1

    dictionary = inverted.get_dictionary()
    i = 0

    for k, v in dictionary.items():
        if i < 10:
            print(k, v)
            i += 1
    inverted.load_dictionary('data/dictionaries/recipes.json')

    dict2 = inverted.get_dictionary()

    i = 0

    for k, v in dict2.items():
        if i < 10:
            print(k, v)
            i += 1


if __name__ == '__main__':
    main()