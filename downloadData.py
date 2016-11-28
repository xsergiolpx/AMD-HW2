import requests
from string import ascii_lowercase
from bs4 import BeautifulSoup
from manageFiles import saveToFile
from manageFiles import loadFromFile

# How many recipes to lookup
totalRecipes = 11232

# List of all the URLs of the places to find the ingredients. There are no ingredients which begin by x
urls = []
for letter in ascii_lowercase:
    if letter is not "x":
        urls.append("http://www.bbc.co.uk/food/ingredients/by/letter/" + letter)

#List of all the URL of the ingredients
ingredientsURL = []

# Collect all ingredients of each webpage of urls
for page in urls:
    cnt = requests.get(page)
    soup = BeautifulSoup(cnt.text, "lxml")
    tmp = soup.find_all(id="foods-by-letter")[0].find_all("a")
    print("Getting the ingredients of", page)
    for i in tmp[:]:
        if "Related " not in str(i):
            ingredientsURL.append("http://www.bbc.co.uk" + str(i).split("\"")[1])
del tmp

# Create dict, keys are links of the ingredients, each value is a list that contains the links of of the recipes that you can make using such ingredient
recipes = set()

# Load visited links from previous runs if any
visitedLinks = loadFromFile("retrieveData/visitedLinks")
# Load the links of the recipes found in previous runs if any
recipes = set(loadFromFile("retrieveData/recipes"))
# Store the links of the type /search? here because the process to get recipe links here is different
searchMore = loadFromFile("retrieveData/searchMore")
# how many ingredients URL have we visited so far
counter = len(visitedLinks)

#Investigate each ingredient URL
for link in ingredientsURL:
    # avoid looking twice in the same link
    if link not in visitedLinks:
        counter += 1
        print("###", counter, "/", len(ingredientsURL) ,"explored ingredients ### Total recipes",  len(recipes)  ,"#### Fetching ---> ", link)
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
            #some ingredients links that lead to /search? so we store them here to analize later
            if "/food/recipes/search" in str(i) and "[]" not in str(i):
                searchMore.append("http://www.bbc.co.uk" + i["href"].replace(" ", "%20"))
        recipes = recipes.union(set(lis))

        # Save the recipes links to a file
        saveToFile(sorted(recipes), "retrieveData/recipes")
        saveToFile(sorted(visitedLinks), "retrieveData/visitedLinks")
        saveToFile(set(searchMore), "retrieveData/searchMore")
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
    if len(recipes) >= totalRecipes:
        break

print("\n\n ------------- Finish! Total recipes:", len(recipes))

