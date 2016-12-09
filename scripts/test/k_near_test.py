from search.indexing.inverted_index import InvertedIndex
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
    words = ["vegetables", "chocolate", "almond", "onion", "aluminio"]
    for word in words:
        for k in range(len(word)):
            if k == 0:
                continue
            else:
                near = " ".join(key for key, _ in inverted.k_near_string(word, k))
                print("[spelling check][tolerance]", word, "k =", k, near)


    ocurr = 0
    for k in dictionary.keys():
        if "-" in k:
            ocurr+=1
    print("[total guion] %0.2f%s"%(100.0*ocurr/len(dictionary.keys()), "%"))

    # salt, garlic, onion, pepper
if __name__ == '__main__':
    main()