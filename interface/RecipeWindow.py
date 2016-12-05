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

        name_label = Label(recipe_frame, text=self.recipe["recipe_name"])
        name_label.grid(row=0, sticky=W)

        author_label = Label(recipe_frame, text=self.recipe["author"])
        author_label.grid(row=1,sticky=W)

        #photo_image = PhotoImage(file=recipe["pic_url"])
        #image = Label(recipe_frame, image=photo_image)
        #image.grid(row=3,sticky=W)

        basic_information = "Preparation time\n" + self.recipe["prep_time"] + "\nCooking time\n" + self.recipe["cooking_time"] \
                            + "\nServes\n" + self.recipe["serves"] + "\nVegetarian\n" + self.recipe["vegetarian"]
        basic_text = Text(recipe_frame, wrap="word")
        basic_text.insert(INSERT, basic_information)
        basic_text.grid(row=5,sticky=W)

        nutritional_information = "Calories\n" + self.recipe["calories"] + "\nProtein\n" + self.recipe["protein"] + "\nCarbs\n" + \
                                  self.recipe["carbs"] + "\nSugars\n" + self.recipe["sugars"] + "\nTotal fat\n" + \
                                  self.recipe["total_fat"] + "\nSaturated fat\n" + self.recipe["saturated_fat"] + "\nFiber\n" + \
                                  self.recipe["fiber"] + "\nSalt\n" + self.recipe["salt"]
        nutritional_text = Text(recipe_frame, wrap="word")
        nutritional_text.insert(INSERT, nutritional_information)
        nutritional_text.grid(row=5,column=1,sticky="w")

        blank_label = Label(recipe_frame, text="")
        blank_label.grid(row=6, column=1, sticky="w")

        ingredients_text = Text(recipe_frame, wrap="word")
        ingredients_text.insert(INSERT, self.recipe["ingredients"])
        ingredients_text.grid(row=7,sticky=W,columnspan=3)

        blank_label = Label(recipe_frame, text="\n\n")
        blank_label.grid(row=8, column=1, sticky="w")

        method_text = Text(recipe_frame, wrap="word")
        method_text.insert(INSERT, self.recipe["method"])
        method_text.grid(row=9,sticky=W,columnspan=3)