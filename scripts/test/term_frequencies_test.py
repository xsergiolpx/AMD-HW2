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

    dictionary = inverted.get_dictionary()
    i = 0

    for k, v in dictionary.items():
        if i < 200:
            print(k, v)
            if k == '':
                continue
            pp.pprint(inverted.load_frequencies('data/term_frequencies/' + k))
            i += 1

if __name__ == '__main__':
    main()


