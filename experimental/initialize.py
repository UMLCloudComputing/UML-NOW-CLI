import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
import argparse
import requests

default_ef = embedding_functions.DefaultEmbeddingFunction()

def embed_text(client, url):
    collection = client.create_collection(name="my_collection", embedding_function=default_ef)
    # URL to fetch the JSON data

    # Make the GET request
    response = requests.get(url)
    data = response.json()


    # Course Titles
    titles = []
    ids = []
    descriptions = []

    for course in data:
        # Find the position of the first open parenthesis
        pos = course["Title"].find('(')
        # Slice the title up to the position of the open parenthesis
        clean_title = course["Title"][:pos].strip() if pos != -1 else course["Title"].strip()
        titles.append(clean_title)
        ids.append(course["Id"] + course['AcademicCareer']['Description'])
    # Create a new database
    

    collection.add(
        documents=titles,
        ids=ids
    )