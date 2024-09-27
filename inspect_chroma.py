# inspect_chroma.py

import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_environment():
    """
    Loads environment variables from the .env file.
    """
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    load_dotenv(dotenv_path)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY not found in environment variables.")
        raise ValueError("The OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    return OPENAI_API_KEY

def connect_chroma(OPENAI_API_KEY):
    """
    Connects to the ChromaDB client.
    """
    persist_directory = os.path.join(os.getcwd(), "chroma_db")
    client = chromadb.PersistentClient(path=persist_directory)
    logger.info("Connected to ChromaDB.")
    return client

def get_collection(client, collection_name="pdf_collection"):
    """
    Retrieves the specified collection from ChromaDB.
    """
    collection = client.get_collection(name=collection_name)
    if not collection:
        logger.error(f"Collection '{collection_name}' does not exist.")
        raise ValueError(f"Collection '{collection_name}' does not exist.")
    logger.info(f"Retrieved collection '{collection_name}'.")
    return collection

def print_documents(collection):
    """
    Retrieves and prints all documents in the collection.
    """
    # Retrieve all documents without including 'ids'
    results = collection.get(include=["documents", "metadatas"])
    documents = results["documents"]
    metadatas = results["metadatas"]

    if not documents:
        logger.warning("No documents found in the collection.")
        return

    for doc, meta in zip(documents, metadatas):
        logger.info(f"Metadata: {meta}")
        logger.info(f"Content:\n{doc}\n{'-'*50}\n")

if __name__ == "__main__":
    try:
        # Step 1: Load environment variables
        OPENAI_API_KEY = load_environment()

        # Step 2: Connect to ChromaDB
        client = connect_chroma(OPENAI_API_KEY)

        # Step 3: Access the collection
        collection = get_collection(client, "pdf_collection")

        # Step 4: Print all documents
        print_documents(collection)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
