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

    # Get postings
    entry = "garlic chicken salt pepper onion water water oliv oil"

    postings = deque(map(lambda x: inverted.retrieve_posting(posting=dictionary[x]["posting"]), entry.split(" ")))

    union = " ".join(k for k, v in inverted.k_near_string("vegetables", 5))
    postings.append(inverted.union(map(lambda x: inverted.retrieve_posting(dictionary[x]["posting"]), union.split())))

    tic = time.time()
    result = set(postings.popleft())
    while len(postings) != 0:
        result = result & set(postings.popleft())

    toc = time.time() - tic
    print(sorted(list(result)))
    print("[sets] size(p1)=", len(result), toc)

    # Get postings
    entry = "vegetables garlic chicken salt pepper onion water water oliv oil"
    tic = time.time()
    sort_list = inverted.intersection_list(entry.split(), 5)
    toc = time.time() - tic
    print(sort_list)
    print("[deque] size(p1)=", len(sort_list), toc)


        # salt, garlic, onion, pepper
if __name__ == '__main__':
    main()