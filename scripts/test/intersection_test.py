from search.indexing.inverted_index import InvertedIndex
import argparse
import time
from collections import deque

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
    parser.add_argument('-p1', '--Posting 1',
                        help='Reference to the posting in postings',
                        dest="p1",
                        required=True)
    parser.add_argument('-p2', '--Posting 2',
                        help='Reference to the posting in postings',
                        dest="p2",
                        required=True)
    parser.add_argument('-d', '--debug',
                        help="Debug is passed.",
                        action="store_true",
                        dest="debug")
    arguments = parser.parse_args()

    return arguments, parser


def main():
    args, parser = get_args()

    inverted = InvertedIndex(name=args.name,
                             filename=args.filename,
                             types=['author', 'ingredients', 'method', 'programme', 'recipe_name'],
                             debug=args.debug)
    # Put dictionary in RAM
    inverted.load_dictionary(args.filename)

    # Get dictionary
    dictionary = inverted.get_dictionary()

    # Get postings
    posting1 = inverted.retrieve_posting(posting=dictionary[args.p1]["posting"])
    posting2 = inverted.retrieve_posting(posting=dictionary[args.p2]["posting"])

    if args.debug:
        # Print intersection
        tic = time.time()
        my_inter = inverted.intersection_array(p1=posting1, p2=posting2)
        toc = time.time() - tic
        print("[intersection] ", my_inter)
        print("[intersection] size(my_inter)=", len(my_inter), "time=", toc)

        # Print intersection
        tic = time.time()
        my_inter = inverted.intersection(p1=deque(posting1), p2=deque(posting2))
        toc = time.time() - tic
        print("[deque] ", my_inter)
        print("[deque] size(my_inter)=", len(my_inter), "time=", toc)

        # Check if we're ok
        tic = time.time()
        intersection = sorted(list(set(posting1).intersection(set(posting2))))
        toc = time.time()-tic
        print("[sets]", intersection)
        print("[sets] size(p1)=",len(posting1), "size(p2)=", len(posting2), "size(p1 and p2)=", len(intersection), "time=", toc)

        # See if they're equal
        print("[merge] ", my_inter == list(intersection))

        # salt, garlic, onion, pepper
if __name__ == '__main__':
    main()