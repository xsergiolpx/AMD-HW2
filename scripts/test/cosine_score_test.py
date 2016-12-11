from search.indexing.inverted_index import InvertedIndex
from search.preprocess.data_processing import clean_string, tokenize
import pprint


def main():
    pp = pprint.PrettyPrinter(indent=3)

    inverted = InvertedIndex(name="recipes",
                             filename="c",
                             types=['author', 'ingredients', 'method', 'programme', 'recipe_name'],
                             debug=True)
    # Put dictionary in RAM
    inverted.load_dictionary("data/dictionaries/recipes.json")

    # Get postings
    entry = "nutella pancake"

    query = tokenize(clean_string(entry))

    for doc, score in inverted.cosine_score(query):
        print(doc, score)

        # salt, garlic, onion, pepper
if __name__ == '__main__':
    main()