from search.indexing.inverted_index import InvertedIndex
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
    entry = "garlic chicken salt pepper onion oliv oil vegetables"

    for doc, score in inverted.cosine_score(entry):
        print(doc, score)

        # salt, garlic, onion, pepper
if __name__ == '__main__':
    main()