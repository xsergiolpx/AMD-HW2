from tkinter import *
from interface import SearchWindow
#from search.indexing.inverted_index import search


class InitialWindow:
    main_window = None

    def __init__(self, root):
        self.main_window = root
        self.create_initial_window()

    def search_event(self, event):
        query = event.widget.get()
        results = search(query)

        root = Tk()
        root.geometry("410x150")
        root.wm_title("Recipes Search")
        SearchWindow.SearchWindow(root, results)
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
             }]

if __name__ == "__main__":
    root = Tk()
    root.geometry("410x150")
    root.wm_title("Recipes Search")
    iw = InitialWindow(root)
    root.mainloop()
