import time

import requests
from bs4 import BeautifulSoup

from search.download.manageFiles import append_to_file
from search.download.manageFiles import load_from_file
from search.download.manageFiles import save_to_tsv
from search.download.manageFiles import delete_file

def isFloat(number):
    '''
    Checks if the number is floatable
    :param number: parameter to check
    :return: True if is float, False if is not
    '''
    try:
        float(number)
        return True
    except ValueError:
        return False

def analizeRecipes(reset = False):

    # filename to write the data
    file="data/data"
    # filename to save the visited recipes to save on the fly
    visitedRecipes = "data/retrieveData/visitedRecipes"
    if reset == True:
        #empty the file visitedRecipes and data.tsv
        delete_file(visitedRecipes + ".txt")
        delete_file(file + ".tsv")

    # list of links of the recipes to examine
    links = load_from_file("data/retrieveData/recipes")
    # load list of already analized links from previous runs if any
    analizedLinks = load_from_file(visitedRecipes)

    # counter of the analized recipes
    counter = len(analizedLinks)

    for link in links:
        if link not in analizedLinks:
            retry = 0
            while retry < 3:
                # try to get the connection, if fails, wait 5 seconds and retry
                try:
                    counter += 1
                    print("###", counter , "of", len(links), "#### Fetching --> " ,link)
                    cnt = requests.get(link)
                    soup = BeautifulSoup(cnt.text, "lxml")

                    # All the information is under this id
                    information = soup.find_all(id="orb-modules")[0]

                    # Add all the information
                    '''
                    header = ["recipe_name", "author", "programme", "prep_time", "cooking_time", "serves", "pic_id",
                    "method", "ingredients", "vegetarian" , "calories", "protein", "carbs", "sugars", "total_fat",
                    "saturated_fat", "fiber", "salt", "link"])
                    '''
                    header=[]

                    # name
                    header.append(information.find_all(itemprop="name")[0].contents[0])

                    # author
                    try:
                        header.append(information.find_all(itemprop="author")[1].contents[0])
                    except IndexError:
                        try:
                            header.append(information.find_all(itemprop="author")[0].contents[0])
                        except IndexError:
                            header.append("NaN")
                    # programme
                    # header.append(str(information.find_all("p")[-4].contents[0]).replace("  ","").replace("\n",""))
                    try:
                        header.append(information.find_all(class_="chef__programme-name")[0].find_all("a")[0].contents[0])
                    except IndexError:
                        header.append("NaN")

                    # prep_time
                    # header.append(information.find_all(itemprop="prepTime")[0].contents[0])
                    try:
                        header.append(information.find_all(class_="recipe-metadata__prep-time")[0].contents[0])
                    except IndexError:
                        header.append("NaN")

                    # cooking_time
                    # header.append(information.find_all(itemprop="cookTime")[0].contents[0])
                    try:
                        header.append(information.find_all(class_="recipe-metadata__cook-time")[0].contents[0])
                    except IndexError:
                        header.append("NaN")

                    # serves
                    try:
                        header.append(information.find_all(itemprop="recipeYield")[0].contents[0])
                    except IndexError:
                        header.append("NaN")
                    # pic url
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
                    # method
                    # contains multiple paragraphs, gotta add them all and puth them together
                    try:
                        methods = information.find_all(itemprop="recipeInstructions")
                        methodText = ""
                        for method in methods:
                            methodText += method.contents[1].contents[0] + " "
                        header.append(methodText)
                    except IndexError:
                        header.append("NaN")

                    # ingredients
                    # some ingredients have information in link form and other information in normal form
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

                    # vegetarian
                    header.append(str("/vegetarian" in str(soup)))

                    # Nutritional content
                    measure = ["kcal", "protein", "carbohydrate", "suars", "fat", "saturates", "fibre", "salt"]
                    # Paragrapth where all the information is contained
                    try:
                        #the replace avoids problems parsnig the data
                        nutrition = information.find_all(itemprop="description")[0].contents[-1].replace(",","").replace(")","").replace("(","").replace("kcal"," kcal ").replace("salt.","salt").replace("carbohydrates","carbohydrate").replace("g","").split()
                        for element in measure:
                            if element in nutrition and element is not " ":
                                ind = nutrition.index(element)
                                mass = nutrition[ind - 1]
                                if isFloat(mass) == True:
                                    header.append(mass)
                                else:
                                    header.append("NaN")
                            else:
                                header.append("NaN")
                    except IndexError:
                        for _ in range(len(measure)):
                            header.append("NaN")
                    # link
                    header.append(link)

                    # Check all fields are non-empty
                    for field in range(len(header)):
                        if len(header[field]) is 0:
                            header[field] = "NaN"
                        if "\t" in header[field] or "\n" in header[field] or "\r" in header[field]:
                            header[field] = header[field].replace("\n", " ").replace("\t", " ").replace("\r", " ")
                    #print(header[10:])
                    # Append current header to the file
                    save_to_tsv(header, file)
                    # Append the visited link ot a file
                    append_to_file(link, visitedRecipes)
                    #Recipe downloaded, go to the next oen
                    break
                except IndexError:
                    # no connection!! retry in 5 seconds
                    print(" tries. No connection, retry in 5 seconds. Tries [", retry + 1, "of", 3, "]")
                    retry += 1
                    time.sleep(5)
                    counter -= 1

#analizeRecipes(False)