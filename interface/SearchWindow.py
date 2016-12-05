from tkinter import *
from interface import RecipeWindow


class SearchWindow:
    main_window = None
    search_sentence = "honey pancake"
    total_results = "22"
    results = None
              #["honey pancake", "american pancake1", "american pancake2", "american pancake3", "american pancake4",
              #        "american pancake5", "american pancake6", "american pancake7", "american pancake8",
              #        "american pancake9", "american pancake10", "american pancake11", "american pancake12"]
    selected = None

    def __init__(self, root, results):
        self.main_window = root
        self.results = results
        self.create_search_window()

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

    def create_search_window(self):
        search_frame = Frame(self.main_window, width=400, height=600)
        search_frame.pack()

        search_label = Label(search_frame, text="Search")
        search_label.pack()

        search_entry = Entry(search_frame)
        search_entry.pack()

        blank_label = Label(search_frame, text="")
        blank_label.pack()

        keyword_label = Label(search_frame, text="Recipes with keyword " + SearchWindow.search_sentence)
        keyword_label.pack()

        total_results_label = Label(search_frame, text=SearchWindow.total_results + " result(s) found")
        total_results_label.pack()

        total_results_listbox = Listbox(search_frame, background='white')
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