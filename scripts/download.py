from search.download.analizeRecipes import analizeRecipes
from search.download.downloadData import downloadData

'''
Script to find the links of the recipes and to download its information.
If reset = True, it deletes all previous downloaded information
'''

#Search for the links of the recipes
downloadData(reset = False)

#Analize the recipes and export to data.tsv
analizeRecipes(reset = False)