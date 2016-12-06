from tkinter import *
from interface import RecipeWindow


class SearchWindow:
    search_entry = None
    previous_window = None
    query = None
    results = None
    selected = None

    def __init__(self, previous_window, query, results):
        self.previous_window = previous_window
        self.results = results
        self.query = query
        self.make_search_window()

    def search_event(self, event):
        query = self.search_entry.get()
        if query.strip() != "":
            results = search(query)
            self.create_search_window(query, results)

    def create_search_window(self, query, results):
        root = Tk()
        root.geometry("410x400")
        root.wm_title("Recipes Search")
        SearchWindow(root, query, results)
        self.previous_window.destroy()
        root.mainloop()

    def listbox_selection(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.selected = self.results[index]

    def create_recipe_window(self, event):
        root = Tk()
        root.wm_title("Recipes Search")
        if self.selected is None:
            self.selected = self.results[0]
        RecipeWindow.RecipeWindow(root, self.selected)
        root.mainloop()

    def make_search_window(self):
        search_frame = Frame(self.previous_window)
        search_frame.pack(side=LEFT, fill=BOTH)

        blank_label = Label(search_frame, text="")
        blank_label.pack()

        search_label = Label(search_frame, text="Search")
        search_label.pack()

        sv = StringVar()
        search_entry = Entry(search_frame, textvariable=sv, width=50)
        search_entry.pack()
        search_entry.bind('<Return>', self.search_event)
        self.search_entry = search_entry
        self.search_entry.insert(index=0,string=self.query)

        go_button = Button(search_frame, text="Go!")
        go_button.bind('<Button-1>', self.search_event)
        go_button.pack()

        blank_label = Label(search_frame, text="")
        blank_label.pack()

        keyword_label = Label(search_frame, text="Recipes with keyword " + self.query)
        keyword_label.pack()

        total_results_label = Label(search_frame, text=str(len(self.results)) + " result(s) found")
        total_results_label.pack()

        total_results_listbox = Listbox(search_frame, background='white', width=50)
        total_results_scrollbar = Scrollbar(total_results_listbox, orient=VERTICAL)
        total_results_listbox.config(selectmode='browse', yscrollcommand=total_results_scrollbar.set)
        total_results_scrollbar.configure(command=total_results_listbox.yview)

        for recipe in self.results:
            total_results_listbox.insert(END, recipe["recipe_name"])

        total_results_scrollbar.pack(side=RIGHT, fill=Y)
        total_results_listbox.pack(side=LEFT, fill=BOTH, expand=1)
        total_results_listbox.bind('<<ListboxSelect>>', self.listbox_selection)

        ok_button = Button(search_frame, text="OK")
        ok_button.pack()
        ok_button.bind('<Button-1>', self.create_recipe_window)


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
             }, {"recipe_name": "soup"}, {"recipe_name": "ba2"}, {"recipe_name": "ba3"}, {"recipe_name": "ba4"}
        , {"recipe_name": "asds"}, {"recipe_name": "sdfs"}, {"recipe_name": "ghf"}]
