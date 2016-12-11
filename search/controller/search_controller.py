from search.preprocess.data_processing import clean_string, tokenize
from search.download.manageFiles import read_json


def retrieve_recipes(inverted, entry):
    results = []
    recipes_dir = "./data/recipes/"
    query = tokenize(clean_string(entry))
    for doc_id,score in inverted.cosine_score(query):
        recipe = read_json(recipes_dir+str(doc_id)+".json")
        results.append(recipe)
    return results