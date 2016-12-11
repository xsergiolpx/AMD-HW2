from tkinter import *
from interface import SearchWindow
from search.controller.search_controller import retrieve_recipes


class InitialWindow:
    main_window = None
    search_entry = None
    inverted = None

    def __init__(self, root, inverted):
        self.main_window = root
        self.create_initial_window()
        self.inverted = inverted

    def search_event(self, event):
        query = self.search_entry.get()
        if query.strip() != "":
            results = retrieve_recipes(self.inverted, query)
            self.create_search_window(query, results)

    def create_search_window(self, query, results):
        root = Tk()
        root.geometry("410x400")
        root.wm_title("Recipes Search")
        SearchWindow.SearchWindow(root, query, results, self.inverted)
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