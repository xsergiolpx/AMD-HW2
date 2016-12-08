from string import ascii_lowercase

import requests
from bs4 import BeautifulSoup
import time

from search.download.manageFiles import load_from_file
from search.download.manageFiles import save_to_file
from search.download.manageFiles import delete_file

def downloadData(reset = False):
    # How many recipes to lookup
    totalRecipes = 11232

    # List of all the URLs of the places to find the ingredients. There are no ingredients which begin by x
    urls = []
    for letter in ascii_lowercase:
        if letter is not "x":
            urls.append("http://www.bbc.co.uk/food/ingredients/by/letter/" + letter)

    # List of all the URL of the ingredients
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

    # Create dict, keys are links of the ingredients, each value is a list that contains the links of of the recipes that
    # you can make using such ingredient
    recipes = set()

    if reset == True:
        delete_file("data/retrieveData/visitedLinks.txt")
        delete_file("data/retrieveData/recipes.txt")
        delete_file("data/retrieveData/searchMore.txt")

    # Load visited links from previous runs if any
    visitedLinks = load_from_file("data/retrieveData/visitedLinks")
    # Load the links of the recipes found in previous runs if any
    recipes = set(load_from_file("data/retrieveData/recipes"))
    # Store the links of the type /search? here because the process to get recipe links here is different
    searchMore = load_from_file("data/retrieveData/searchMore")
    # how many ingredients URL have we visited so far
    counter = len(visitedLinks)

    # Investigate each ingredient URL
    for link in ingredientsURL:
        # avoid looking twice in the same link
        if link not in visitedLinks:
            counter += 1
            print("###", counter, "/", len(ingredientsURL) ,"explored ingredients ### Total recipes",  len(recipes)  ,"#### Fetching ---> ", link)
            visitedLinks.append(link)
            while True:
                try:
                    cnt = requests.get(link)
                    soup = BeautifulSoup(cnt.text, "lxml")
                    tmp = soup.find_all(id="subcolumn-1")[0].find_all("a", href=True)
                    break
                except IndexError:
                    print("No connection, sleep 5 seconds")
                    time.sleep(5)
            # Create the list of all the recipes inside one ingredient page
            lis = []
            # save only recipes links
            for i in tmp[:]:
                if "all recipes using " not in str(i) and "search" not in str(i):
                    lis.append("http://www.bbc.co.uk" + i["href"])
                # some ingredients links that lead to /search? so we store them here to analize later
                if "/food/recipes/search" in str(i) and "[]" not in str(i):
                    searchMore.append("http://www.bbc.co.uk" + i["href"].replace(" ", "%20"))
            recipes = recipes.union(set(lis))

            # Save the recipes links to a file
            save_to_file(sorted(recipes), "data/retrieveData/recipes")
            save_to_file(sorted(visitedLinks), "data/retrieveData/visitedLinks")
            save_to_file(set(searchMore), "data/retrieveData/searchMore")

    # Now we have to search in urls like /food/recipes/search?keywords=rice
    for search in searchMore:
        maxPage = 1
        counterPage = 0
        if search not in visitedLinks:
            cnt = requests.get(search)
            soup = BeautifulSoup(cnt.text, "lxml")

            # Try to get maximum number of webpages
            try:
                maxPage = soup.find_all(class_="see-all-search")[-2].contents[0]
                searchPages = [search[:41] + "page=" + str(i) + "&" + search[41:] for i in range(1, int(maxPage) + 1)]
            except IndexError:
                # Then the search webpage offers only one page for the results
                searchPages = [search]

            # investigate each page of maxPage
            for searchI in searchPages:
                counterPage += 1
                cnt = requests.get(searchI)
                soup = BeautifulSoup(cnt.text, "lxml")
                elementsLeft = soup.find_all(class_="left")

                # Add here all the found recipes in each page
                lis = []
                for i in elementsLeft:
                    lis.append("http://www.bbc.co.uk" + i.find_all("a")[0]["href"])
                    recipes = recipes.union(set(lis))
                print(len(recipes), "of", totalRecipes, " Recipes ### Retrieving page -->", counterPage, "of", maxPage, searchI)
                save_to_file(sorted(recipes), "data/retrieveData/recipes")
                if len(recipes) >= totalRecipes:
                    visitedLinks.append(search)
                    break
            visitedLinks.append(search)
            save_to_file(sorted(visitedLinks), "data/retrieveData/visitedLinks")
            if len(recipes) >= totalRecipes:
                break
        if len(recipes) >= totalRecipes:
            break

    print("\n\n ------------- Finish! Total recipes:", len(recipes))

