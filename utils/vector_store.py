# utils/vector_store.py

import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import logging

from utils.logger import setup_logging

# Initialize logging
setup_logging()

# Load environment variables
load_dotenv()

# Set OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY not found in environment variables.")
    raise ValueError("The OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

def get_chroma_client():
    """
    Initializes and returns a persistent ChromaDB client.
    """
    persist_directory = os.path.join(os.getcwd(), "chroma_db")
    client = chromadb.PersistentClient(path=persist_directory)
    logging.info("Initialized ChromaDB client.")
    return client

def create_collection(client, collection_name):
    """
    Creates or retrieves a ChromaDB collection with the specified embedding function.

    :param client: ChromaDB client instance.
    :param collection_name: Name of the collection.
    :return: ChromaDB collection instance.
    """
    # Instantiate the built-in OpenAI embedding function
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-ada-002"  # You can change the model as needed
    )

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=openai_ef  # Use the built-in embedding function
    )
    logging.info(f"Collection '{collection_name}' is ready.")
    return collection

def add_documents(collection, documents, metadatas, ids):
    """
    Adds documents to a ChromaDB collection after validating them.

    :param collection: ChromaDB collection instance.
    :param documents: List of document texts.
    :param metadatas: List of metadata dictionaries.
    :param ids: List of unique IDs for each document.
    """
    # Validate documents
    valid_documents = []
    valid_metadatas = []
    valid_ids = []

    for doc, meta, id_ in zip(documents, metadatas, ids):
        if isinstance(doc, str) and doc.strip():
            valid_documents.append(doc.strip())
            valid_metadatas.append(meta)
            valid_ids.append(id_)
        else:
            logging.warning(f"Skipping invalid or empty document with ID: {id_}")
            print(f"Skipping invalid or empty document with ID: {id_}")

    if not valid_documents:
        error_message = "No valid documents to add."
        logging.error(error_message)
        raise ValueError(error_message)

    # Debug: Log documents being added
    for doc in valid_documents:
        logging.info(f"Adding document: {doc[:100]}...")  # Logs the first 100 characters

    try:
        collection.add(
            documents=valid_documents,
            metadatas=valid_metadatas,
            ids=valid_ids
        )
        logging.info(f"Successfully added {len(valid_documents)} documents to the collection.")
    except Exception as e:
        logging.error(f"Failed to add documents to ChromaDB: {e}")
        raise e

def query_collection(collection, query_text, n_results=5):
    """
    Queries the ChromaDB collection for relevant documents.

    :param collection: ChromaDB collection instance.
    :param query_text: The query string.
    :param n_results: Number of results to retrieve.
    :return: Query results containing relevant documents.
    """
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        logging.info(f"Query executed successfully. Retrieved {len(results['documents'][0])} documents.")
        return results
    except Exception as e:
        logging.error(f"Failed to query collection: {e}")
        raise e
