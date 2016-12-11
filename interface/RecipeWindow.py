from tkinter import *


class RecipeWindow(Frame):

    recipe = {
        "recipe_name",
        "author",
        "programme",
        "prep_time",
        "cooking_time",
        "serves",
        "pic_url",
        "method",
        "ingredients",
        "vegetarian",
        "calories",
        "protein",
        "carbs",
        "sugars",
        "total_fat",
        "saturated_fat",
        "fiber",
        "salt",
        "link"
    }

    def __init__(self, root, recipe):
        self.recipe = recipe
        self.create_recipe_frame(root)

    def create_recipe_frame(self, root):
        recipe_frame = Frame(root, background="white")
        recipe_frame.grid(row=0)

        name_label = Label(recipe_frame, text=self.recipe["recipe_name"], bg="white")
        name_label.grid(row=0, sticky=W)

        author_label = Label(recipe_frame, text=self.recipe["author"], bg="white")
        author_label.grid(row=1,sticky=W)

        basic_information = "Preparation time: " + self.recipe["prep_time"] + "\nCooking time: " + self.recipe["cooking_time"] \
                            + "\nServes: " + self.recipe["serves"] + "\nVegetarian: " + str(self.recipe["vegetarian"])
        basic_text = Text(recipe_frame, wrap="word", height=10, width=20)
        basic_text.insert(INSERT, basic_information)
        basic_text.grid(row=5,sticky=W)

        nutritional_information = "Calories: " + str(self.recipe["calories"]) + "\nProtein: " + str(self.recipe["protein"]) + "\nCarbs: " + \
                                  str(self.recipe["carbs"]) + "\nSugars: " + str(self.recipe["sugars"]) + "\nTotal fat: " + \
                                  str(self.recipe["total_fat"]) + "\nSaturated fat: " + str(self.recipe["saturated_fat"]) + "\nFiber: " + \
                                  str(self.recipe["fiber"]) + "\nSalt: " + str(self.recipe["salt"])
        nutritional_text = Text(recipe_frame, wrap="word", height=10, width=20)
        nutritional_text.insert(INSERT, nutritional_information)
        nutritional_text.grid(row=5,column=1,sticky="w")

        ingredient_label = Label(recipe_frame, text="Ingredients", bg="white")
        ingredient_label.grid(row=6, sticky="w")

        ingredients_text = Text(recipe_frame, wrap="word", height=15, width=50)
        ingredients_text.insert(INSERT, self.recipe["ingredients"])
        ingredients_text.grid(row=7,sticky=W,columnspan=2)

        methods_label = Label(recipe_frame, text="Methods", bg="white")
        methods_label.grid(row=8, sticky="w")

        method_text = Text(recipe_frame, wrap="word", height=20, width=50)
        method_text.insert(INSERT, self.recipe["method"])
        method_text.grid(row=9,sticky=W,columnspan=2)