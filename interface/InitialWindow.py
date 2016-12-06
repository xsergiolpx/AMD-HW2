from tkinter import *
from interface import SearchWindow
#from search.indexing.inverted_index import search


class InitialWindow:
    main_window = None
    search_entry = None

    def __init__(self, root):
        self.main_window = root
        self.create_initial_window()

    def search_event(self, event):
        query = self.search_entry.get()
        if query.strip() != "":
            results = search(query)
            self.create_search_window(query, results)

    def create_search_window(self, query, results):
        root = Tk()
        root.geometry("410x400")
        root.wm_title("Recipes Search")
        SearchWindow.SearchWindow(root, query, results)
        self.main_window.destroy()
        root.mainloop()

    def create_initial_window(self):
        blank_label = Label(self.main_window, text="\n\n")
        blank_label.grid(row=0)

        search_label = Label(self.main_window, text="Search", width=50)
        search_label.grid(row=1, column=1)

        sv = StringVar()
        search_entry = Entry(self.main_window, textvariable=sv, width=50)
        search_entry.grid(row=2, columnspan=4)
        search_entry.bind('<Return>', self.search_event)
        self.search_entry = search_entry

        go_button = Button(self.main_window, text="Go!")
        go_button.bind('<Button-1>', self.search_event)
        go_button.grid(row=2, column=4)


def search(query):
    return [{"recipe_name": "soup",
             "author": "eu",
             "programme": "ana maria",
             "prep_time": "10",
             "cooking_time": "9",
             "serves": "1",
             "pic_url": "/home/gabriel/Documents/1_Semester/ADM/HW2/interface/recipe.gif",
             "method": "Put the dried mushrooms in a large, heavy-based saucepan and cover with the water.",
             "ingredients": "15g/½oz dried wild mushrooms, such as porcini\n1.4 litres/2½ pints just-boiled water",
             "vegetarian": "V",
             "calories": "55",
             "protein": "10",
             "carbs": "12",
             "sugars": "9",
             "total_fat": "7",
             "saturated_fat": "3",
             "fiber": "2",
             "salt": "0.5"
             }, {"recipe_name": "soup"}, {"recipe_name": "soup2"}, {"recipe_name": "soup3"}, {"recipe_name": "soup4"}
        , {"recipe_name": "soup5"}, {"recipe_name": "soup6"}, {"recipe_name": "soup7"}]

if __name__ == "__main__":
    root = Tk()
    root.geometry("460x150")
    root.wm_title("Recipes Search")
    iw = InitialWindow(root)
    root.mainloop()