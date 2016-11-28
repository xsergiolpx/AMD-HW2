Hello world!

# Functions description

downloadData.py: gets all the link recipes of the website. First it looks in /food/ingredients/ for all the recipes that are linked from a ingredient page. Then it looks up the recipes that aren't there but are on /search?keyword=. Stores the links in the files ./retrieveData/recipes.txt. Also in order to continue searching for links, if the conection is interrupted, all the visited links are stored in ./retrieveData/visitedLinks.txt and ./retrieveData/searchMore.txt (the first are the /food/ingredients/ links and the second the /search?keyword=). The links are saved on the fly as the machine retrieves the information.

analizeRecipes.py: reads URLs of the file ./retrieveData/recipes.txt and extracts the following information of each recipe:
header = ["recipe_name", "author", "programme", "prep_time", "cooking_time", "serves", "pic_url", "method", "ingredients", "vegetarian = True or False" , "calories", "protein", "carbs", "sugars", "total_fat", "saturated_fat", "fiber", "salt", "link"])

When a value is missing, it is replaced by NaN, except for the image, that shows the URL of a unknkown dish. Nutritional values are shown in kcal or grams. This info is saved on data.tsv on the fly as the machine visits each link. If the conection is rejected, it waits 3 seconds before doing an other petition to the server. If the machine goes down, the progress is automatically saved on the file ./retrieveData/visitedRecipes so it continues from the same point the next time the program is ran.

manageFiles.py is a library that is used to save the links to the HDD and to load them.
