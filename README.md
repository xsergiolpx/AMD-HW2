# Search Engine on BBC webpage

[![Python](https://img.shields.io/badge/python-3.5.2-brightgreen.svg)](https://docs.python.org/3.5/whatsnew/changelog.html#python-3-5-2)

## Description

This software is able to find and download and parse more than 11.000 dish recipes from the [BBC webpage](http://www.bbc.co.uk/food/) and allows to look up all the recipes that can be used with specific ingredients using the inverted index of the downloaded data.

## How to run it

In order to download or update the dish recipes the file scripts/download.py should be ran:

```
python scripts/download.py
```

To preprocess the data use the following command:

```
python search/preprocess/data_processing.py
```

The search engine can bu ran from the file "Main.py"
