import requests
from string import ascii_lowercase
from bs4 import BeautifulSoup
from manageFiles import saveToFile
from manageFiles import loadFromFile

totalRecipes = 11232

# List of all the URLs of the ingredients. There are no ingredients which begin by x
urls = []
for letter in ascii_lowercase:
    #change when finish
    if letter is not "x":
    #if letter is "a":
        urls.append("http://www.bbc.co.uk/food/ingredients/by/letter/" + letter)


ingredientsURL = []

# Collect all ingredients of each webpage of urls
for page in urls:
    cnt = requests.get(page)
    soup = BeautifulSoup(cnt.text, "lxml")
    tmp = soup.find_all(id="foods-by-letter")[0].find_all("a")
    print("Getting the ingredients of", page)
    for i in tmp[:]:
        if "Related " not in str(i):
            #ingredients.append(str(i).split("        ")[3])
            ingredientsURL.append("http://www.bbc.co.uk" + str(i).split("\"")[1]) #alternative way
del tmp

# Create dict, keys are links of the ingredients, each value is a list that contains the links of of the recipes that you can make using such ingredient
recipes = set()

# Load visited links from previous ran
visitedLinks = loadFromFile("retrieveData/visitedLinks")
#visitedLinks = [] #descomentar para acabar
#Load precious recipes
recipes = set(loadFromFile("retrieveData/recipes"))
#Further search recipes here
searchMore = loadFromFile("retrieveData/searchMore")

#Investigate each ingredient
#ingredientsURL = ["http://www.bbc.co.uk/food/almond"]
counter = len(visitedLinks)
for link in ingredientsURL:
    if link not in visitedLinks:
        counter += 1
        print("######", counter, "/", len(ingredientsURL) ," ingredients explored ### Total recipes",  len(recipes)  ,"#### Fetching ---> ", link)
        visitedLinks.append(link)
        cnt = requests.get(link)
        soup = BeautifulSoup(cnt.text, "lxml")
        tmp = soup.find_all(id="subcolumn-1")[0].find_all("a", href=True)
        # Create the list of all the recipes inside one ingredient page
        lis = []
        # save only recipes links
        for i in tmp[:]:
            if "all recipes using " not in str(i) and "search" not in str(i):
                lis.append("http://www.bbc.co.uk" + i["href"])
            if "/food/recipes/search" in str(i) and "[]" not in str(i):
                searchMore.append("http://www.bbc.co.uk" + i["href"].replace(" ", "%20"))
                print("Gotta investigate this -->",searchMore[-1])
        recipes = recipes.union(set(lis))

        # Save the recipes links to a file
        saveToFile(sorted(recipes), "retrieveData/recipes")
        saveToFile(sorted(visitedLinks), "retrieveData/visitedLinks")
        print(searchMore)
        saveToFile(searchMore, "retrieveData/visitedLinks")
        #time.sleep(0.5)

# Now we have to search in urls like /food/recipes/search?keywords=rice
for search in searchMore:
    maxPage = 1
    counterPage = 0
    if search not in visitedLinks:
        cnt = requests.get(search)
        soup = BeautifulSoup(cnt.text, "lxml")

        #Try to get maximum number of webpages
        try:
            maxPage = soup.find_all(class_="see-all-search")[-2].contents[0]
            searchPages = [search[:41] + "page=" + str(i) + "&" + search[41:] for i in range(1, int(maxPage) + 1)]
        except IndexError:
            searchPages = [search]

        #investigate each page of maxPage
        for searchI in searchPages:
            counterPage += 1
            cnt = requests.get(searchI)
            soup = BeautifulSoup(cnt.text, "lxml")
            elementsLeft = soup.find_all(class_="left")

            #Add here all the found recipes in each page
            lis = []
            for i in elementsLeft:
                lis.append("http://www.bbc.co.uk" + i.find_all("a")[0]["href"])
                recipes = recipes.union(set(lis))
            print(len(recipes), "of", totalRecipes, "### Retrieving page -->", counterPage, "of", maxPage, searchI)
            saveToFile(sorted(recipes), "retrieveData/recipes")
            if len(recipes) >= totalRecipes:
                visitedLinks.append(search)
                break
        visitedLinks.append(search)
        saveToFile(sorted(visitedLinks), "retrieveData/visitedLinks")
        if len(recipes) >= totalRecipes:
            break

print("\n\n ------------- Finish! Total recipes:", len(recipes))

