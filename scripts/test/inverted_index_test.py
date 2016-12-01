from search.indexing.inverted_index import InvertedIndex
import argparse

# TODO: Add options to decide what to do

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', 
                        help='Filename of the tokens. It should be in data.',
                        dest="filename", 
                        required=True)
    parser.add_argument('-s', '--store',
                        help="Do we store postings?",
                        action="store_true",
                        dest="store")
    parser.add_argument('-d', '--debug',
                        help="Debug is passed.",
                        action="store_true",
                        dest="debug")
    arguments = parser.parse_args()
    
    return arguments, parser

def main():
    args, parser = get_args()

    inverted = InvertedIndex(filename=args.filename,
                             types=['author', 'ingredients', 'method', 'programme', 'recipe_name'],
                             debug=args.debug)

    inverted.obtain_tokens()
    inverted.sort_tokens()
    inverted.create_postings()
    
    if args.store:
        inverted.store_postings()

    postings = inverted.get_postings()

    i = 0

    for k, v in postings.items():
        if i < 200:
            print(k, v)
            i += 1


if __name__ == '__main__':
    main()