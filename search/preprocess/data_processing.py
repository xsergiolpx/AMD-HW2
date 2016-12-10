import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter
from search.download.manageFiles import save_to_tsv
from math import sqrt
import string
import re
import sys


def clean_string(text, stemming=True):
    """
    Receives a text, which could be a single word or a sentence, and applies the natural language
    process (using NLTK library) in the text, normalizing, tokenizing, removing stopwords and punctuations,
    stemming and ignoring the duplicated tokens.
    :param text: it is a string, which could be a word or a sentence
    :return: a list containing the tokens
    """

    if pd.isnull(text) or isinstance(text, bool):
        return text

    stopset = set(stopwords.words('english'))
    ps = PorterStemmer()

    # normalize the text
    text = text.lower()

    # substitute a / for a space, in order that they will be split in two tokens
    text = re.sub(r"/", ' ', text)

    # Delete fractions
    fractions = ['̶', '½', '¾', '¼', '⅓', '⅙', '⅛', '⅔', '⅝', '⅜', '—', '–', '‘', '”', '…', '.', '`', '’', '“']
    text = re.sub(('[' + ','.join(map(lambda x: str(x), fractions)) + ']'), '', text)

    # creates the tokens
    text = word_tokenize(text)

    # excludes tokens which contain numbers and punctuations
    text = [t for t in text if bool(re.search(r'\d', t)) == False and t not in string.punctuation]

    # Stemming
    if stemming:
        text = [ps.stem(t) for t in text]

    # Remove stopwords
    text = [t for t in text if not t in stopset]

    # remove the strange character ' appearing before some words
    text = [re.sub('[\'\"]', '', t) for t in text]
    # remove the duplicates before returning the tokens
    return text


def tokenize(text):
    return list(set(text))


def update_frequencies(counter, index):
    sum = 0
    for x, v in counter.items():
        sum += v*v
        save_to_tsv([str(index), str(v)], filename='data/term_frequencies/' + x)
    return sqrt(sum)


def tokenize_csv(filename='data/data.tsv',
                 columns=["recipe_name", "author", "programme", "method", "ingredients"],
                 stemming=[],
                 term_frequencies=True):
    """
    It receives a CSV file in FILENAME containing the recipes in each row and tab-separated. It applies the
    function 'tokenize' in each cell of COLUMNS of the CSV file. It returns a Pandas dataframe.
    :param filename: TSV file containing the recipes. If nothing is specified, them it will try to open 'data.tsv' in
     the current directory
    :param columns: It is a list containing the column names of FILENAME where the function 'tokenize' will be applied
    :return: a Pandas dataframe where each row is a recipe containing the tokens of each column of COLUMNS
    """
    names = ["recipe_name", "author", "programme", "prep_time", "cooking_time", "serves", "pic_url",
              "method", "ingredients", "vegetarian", "calories", "protein", "carbs", "sugars",
              "total_fat", "saturated_fat", "fiber", "salt", "link"]
    df_recipes = pd.read_csv(filename, delimiter="\t", names=names, usecols=columns)

    # Iterates over each row of the recipes dataframe, getting the row and the row number (index)
    N = df_recipes.shape[0]
    with open("data/documents.csv", 'w') as file_t:
        file_t.write(str(N))

    length_file = open("data/length.tsv", "a")

    for index, row in df_recipes.iterrows():
        if term_frequencies:
            counter = Counter()

        if index % 100 == 0:
            print("[preprocessing] %0.2f%s processed (%d of %d)"%(100*index/N,'%', index+1, N))
            sys.stdout.flush()

        # Reads each column name in COLUMNS
        for column in columns:
            # Accesses each cell by the row number and the column name and apply the function tokenize on the cell,
            # changing the value of it by the list of tokens

            if str(row[column]) == 'nan':
                row[column] = ""

            # Use column name inside stemming vector if you dont want stemming in that column
            # raw_row = clean_string(row[column], stemming=False) if column in stemming else clean_string(row[column])
            raw_row = clean_string(row[column])

            if term_frequencies:
                counter.update(raw_row)

            df_recipes.set_value(index, column, list(set(raw_row)))

        if term_frequencies:
            length_file.write("\t".join([str(index), str(update_frequencies(counter, index))]))
            length_file.write("\n")
    length_file.close()

    return df_recipes


def generate_json(df_recipes):
    """
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
    """
    df_recipes.to_json("data/tokens.json", orient="index", force_ascii=False)