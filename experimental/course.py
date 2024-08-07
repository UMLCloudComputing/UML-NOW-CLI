import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.utils import embedding_functions
import argparse

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from umlnow import *

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="ChromaDB")

if __name__ == "__main__":
    #embed_text(client)
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


