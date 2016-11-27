import requests
from bs4 import BeautifulSoup
from manageFiles import saveToTSF
from manageFiles import loadFromFile
from manageFiles import apendToFile


file="data"
visitedRecipes = "retrieveData/visitedRecipes"
links = loadFromFile("retrieveData/recipes")

analizedLinks = loadFromFile(visitedRecipes)

#counter
counter = len(visitedRecipes)

for link in links:
    counter += 1
    if link not in analizedLinks:
        print("###", counter , "of", len(links), "#### Fetching --> " ,link)
        cnt = requests.get(link)
        soup = BeautifulSoup(cnt.text, "lxml")

        # All the information is under this id
        information = soup.find_all(id="orb-modules")[0]

        #Add all the information
        '''
        header = ["recipe_name", "author", "programme", "prep_time", "cooking_time", "serves", "pic_id",
        "method", "ingredients", "vegetarian" , "calories", "protein", "carbs", "total_fat",
        "saturated_fat", "fiber", "salt", "link"])
        '''
        header = []

        # name
        header.append(information.find_all(itemprop="name")[0].contents[0])

        #author
        try:
            header.append(information.find_all(itemprop="author")[1].contents[0])
        except IndexError:
            try:
                header.append(information.find_all(itemprop="author")[0].contents[0])
            except IndexError:
                header.append("NaN")
        #programme
        #header.append(str(information.find_all("p")[-4].contents[0]).replace("  ","").replace("\n",""))
        try:
            header.append(information.find_all(class_="chef__programme-name")[0].find_all("a")[0].contents[0])
        except IndexError:
            header.append("NaN")

        #prep_time
        #header.append(information.find_all(itemprop="prepTime")[0].contents[0])
        header.append(information.find_all(class_="recipe-metadata__prep-time")[0].contents[0])

        #cooking_time
        #header.append(information.find_all(itemprop="cookTime")[0].contents[0])
        header.append(information.find_all(class_="recipe-metadata__cook-time")[0].contents[0])

        #serves
        try:
            header.append(information.find_all(itemprop="recipeYield")[0].contents[0])
        except IndexError:
            header.append("NaN")
        #pic url
        try:
            websitePic = information.find_all(itemprop="image")[0]["src"]
            if websitePic[1] is "t":
                header.append(websitePic)
            elif websitePic[1] is "/":
                header.append("http:" + websitePic)
            else:
                header.append(websitePic)
        except IndexError:
            header.append("http://www.ballesteros.me/amd/unknown.png")
        #method
        #contains multiple paragraphs, gotta add them all and puth them together
        methods = information.find_all(itemprop="recipeInstructions")
        methodText = ""
        for method in methods:
            methodText += method.contents[1].contents[0] + " "
        header.append(methodText)

        #ingredients
        #some ingredients have information in link form and other information in normal form
        ingredients = information.find_all(itemprop="ingredients")
        ingredientText = ""
        for ingredient in ingredients:
            for chunk in ingredient:
                if "href=" not in str(chunk):
                    ingredientText += chunk
                if "href=" in str(chunk):
                    ingredientText += chunk.contents[0]
            ingredientText += ", "
        header.append(ingredientText[:-2])

        #vegetarian
        header.append(str("/vegetarian" in str(soup)))

        #Nutritional content
        measure = ["kcal,", "protein,", "carbohydrate", "sugars),", "fat", "saturates),", "fibre", "salt"]
        #Paragrapth where all the information is contained
        try:
            nutrition = information.find_all(itemprop="description")[0].contents[-1].split()
            for element in measure:
                if element in nutrition:
                    ind = nutrition.index(element)
                    header.append(nutrition[ind - 1].strip("g"))
                else:
                    header.append("NaN")
        except IndexError:
            for _ in range(len(measure)):
                header.append("NaN")
        #link
        header.append(link)

        #Check all fields are non-empty
        for field in range(len(header)):
            if len(header[field]) is 0:
                header[field] = "NaN"
            if "\t" in header[field] or "\n" in header[field] or "\r" in header[field]:
                header[field] = header[field].replace("\n", " ").replace("\t", " ").replace("\r", " ")

        #print(header)

        # Append current header to the file
        saveToTSF(header, file)
        # Append the visited link ot a file
        apendToFile(link, visitedRecipes)