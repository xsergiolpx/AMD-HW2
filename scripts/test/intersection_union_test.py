from search.indexing.inverted_index import InvertedIndex
import time
from collections import deque
import pprint


def main():
    pp = pprint.PrettyPrinter(indent=3)
    inverted = InvertedIndex(name="recipes",
                             filename="c",
                             types=['author', 'ingredients', 'method', 'programme', 'recipe_name'],
                             debug=True)
    # Put dictionary in RAM
    inverted.load_dictionary("data/dictionaries/recipes.json")

    # Get dictionary
    dictionary = inverted.get_dictionary()

    # Get postings
    entry = "garlic chicken salt pepper onion water oliv oil"


    print(inverted.load_posting(posting=dictionary["garlic"]["posting"]))
    print(inverted.load_posting(posting=dictionary["garlic"]["posting"])[1:])
    print(len(inverted.load_posting(posting=dictionary["garlic"]["posting"])[1:]))

    postings = deque(map(lambda x: inverted.load_posting(posting=dictionary[x]["posting"])[1:], entry.split(" ")))

    union = " ".join(k for k, v in inverted.k_near_string("vegetables", 5))
    postings.append(inverted.union(map(lambda x: inverted.load_posting(dictionary[x]["posting"])[1:], union.split())))

    tic = time.time()
    result = set(postings.popleft())
    while len(postings) != 0:
        result = result & set(postings.popleft())

    toc = time.time() - tic
    print(sorted(list(result)))
    print("[sets] size(p1)=", len(result), toc)

    # Get postings
    entry = "garlic chicken salt pepper onion oliv oil vegetables"
    tic = time.time()
    sort_list = inverted.intersection_list(entry.split(), 5)
    toc = time.time() - tic
    print(sort_list)
    print("[deque] size(p1)=", len(sort_list), toc)
        # salt, garlic, onion, pepper
if __name__ == '__main__':
    main()