from search.indexing.inverted_index import InvertedIndex
import argparse
import time
from collections import deque


def main():
    inverted = InvertedIndex(name="recipes",
                             filename="c",
                             types=['author', 'ingredients', 'method', 'programme', 'recipe_name'],
                             debug=True)
    # Put dictionary in RAM
    inverted.load_dictionary("data/dictionaries/recipes.json")

    # Get dictionary
    dictionary = inverted.get_dictionary()

    # Get union postings
    union = " ".join(k for k, v in inverted.k_near_string("vegetables", 5))

    print("[union] Print postings")
    for posting in map(lambda x: inverted.retrieve_posting(posting=dictionary[x]["posting"]), union.split(" ")):
        print(posting)

    print("[union] Print union")
    union = inverted.union(map(lambda x: inverted.retrieve_posting(posting=dictionary[x]["posting"]), union.split(" ")))
    print(union)
    print("[union] len(union)=", len(union))


if __name__ == '__main__':
    main()