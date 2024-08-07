import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
import argparse
default_ef = embedding_functions.DefaultEmbeddingFunction()

import requests


# Initialize ChromaDB client
client = chromadb.PersistentClient(path="ChromaDB")


def embed_text(client):
    collection = client.create_collection(name="my_collection", embedding_function=default_ef)
    # URL to fetch the JSON data
    url = "https://www.uml.edu/api/registrar/course_catalog/v1.0/courses?field=subject&query=COMP"

    # Make the GET request
    response = requests.get(url)
    data = response.json()


    # Course Titles
    titles = []
    ids = []
    descriptions = []

    for course in data:
        titles.append(course["Title"])
        ids.append(course["Id"] + course['AcademicCareer']['Description'])
    # Create a new database
    

    collection.add(
        documents=titles,
        ids=ids
    )

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Query the course collection.")
    parser.add_argument("query", type=str, help="The query text to search for.")
    
    # Parse arguments
    args = parser.parse_args()

    collection = client.get_collection(name="my_collection")
    
    # Use the parsed argument in the query
    results = collection.query(
        query_texts=[args.query],
        n_results=7
    )

    print(results['documents'])


