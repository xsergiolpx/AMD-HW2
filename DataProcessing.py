import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import re


def tokenize(text):
    '''
    Receives a text, which could be a single word or a sentence, and applies the natural language
    process (using NLTK library) in the text, normalizing, tokenizing, removing stopwords and punctuations,
    stemming and ignoring the duplicated tokens.
    :param text: it is a string, which could be a word or a sentence
    :return: a list containing the tokens
    '''

    if pd.isnull(text) or isinstance(text, bool):
        return text

    stopset = set(stopwords.words('english'))
    ps = PorterStemmer()

    # normalize the text
    text = text.lower()

    # creates the tokens
    text = nltk.word_tokenize(text)

    # excludes tokens which contain numbers and punctuations
    text = [t for t in text if bool(re.search(r'\d', t)) == False and t not in string.punctuation]

    # removes the stopwords and punctuations
    text = [ps.stem(t) for t in text]

    # stems the content
    text = [t for t in text if not t in stopset]

    #remove the duplicates before returning the tokens
    return list(set(text))


def tokenize_CSV(filename='data.tsv',
                 columns=["recipe_name", "author", "programme", "method", "ingredients", "vegetarian"]):
    '''
    It receives a CSV file in FILENAME containing the recipes in each row and tab-separated. It applies the
    function 'tokenize' in each cell of COLUMNS of the CSV file. It returns a Pandas dataframe.
    :param filename: TSV file containing the recipes. If nothing is specified, them it will try to open 'data.tsv' in
     the current directory
    :param columns: It is a list containing the column names of FILENAME where the function 'tokenize' will be applied
    :return: a Pandas dataframe where each row is a recipe containing the tokens of each column of COLUMNS
    '''
    names = ["recipe_name", "author", "programme", "prep_time", "cooking_time", "serves", "pic_url",
              "method", "ingredients", "vegetarian", "calories", "protein", "carbs", "sugars",
              "total_fat", "saturated_fat", "fiber", "salt", "link"]
    df_recipes = pd.read_csv(filename, delimiter="\t", names=names, usecols=columns)

    # Iterates over each row of the recipes dataframe, getting the row and the row number (index)
    for index, row in df_recipes.iterrows():
        # Reads each column name in COLUMNS
        for column in columns:
            # Accesses each cell by the row number and the column name and apply the function tokenize on the cell,
            # changing the value of it by the list of tokens
            df_recipes.set_value(index,column, tokenize(row[column]))
    return df_recipes


def generate_json(df_recipes):
    '''
    Receives a Pandas dataframe with the recipes in each row and creates a file tokens.json in the current directory
    with the recipes separated by row. The JSON file has a list-like structure indexed by the row number.
    Ex:
    {
       "0": {
          "recipe_name": ["paella"],
          "author": ["sanjeev","bhaskar"]
       },
       "1": {
          "recipe_name": ["easi","chocol","cake"],
          "author": ["rachel","manley"]
       }
    }
    :param df_recipes: Pandas dataframe with one recipe in each row
    :return:
    '''
    df_recipes.to_json("./tokens.json", orient="index", force_ascii=False)

generate_json(tokenize_CSV())
