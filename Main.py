from search.indexing.inverted_index import InvertedIndex
from tkinter import *
from interface.InitialWindow import InitialWindow


def main():
    inverted = InvertedIndex(name="recipes",
                             filename="c",
                             types=['author', 'ingredients', 'method', 'programme', 'recipe_name'],
                             debug=True)
    # Put dictionary in RAM
    inverted.load_dictionary("data/dictionaries/recipes.json")

    root = Tk()
    root.geometry("460x150")
    root.wm_title("Recipes Search")
    InitialWindow(root, inverted)
    root.mainloop()

if __name__ == "__main__":
    main()