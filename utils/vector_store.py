import os
import chromadb
from chromadb.utils import embedding_functions

def get_chroma_client():
    """
    Initializes and returns a persistent ChromaDB client.
    
    :return: ChromaDB persistent client instance.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("The OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    
    persist_directory = os.path.join(os.getcwd(), "chroma_db")
    
    # Initialize the persistent client
    client = chromadb.PersistentClient(path=persist_directory)
    return client

def create_collection(client, collection_name):
    """
    Creates or retrieves a collection in ChromaDB with the specified embedding function.
    
    :param client: ChromaDB client instance.
    :param collection_name: Name of the collection.
    :return: ChromaDB collection instance.
    """
    # Define the embedding function using OpenAI
    openai_embed = embedding_functions.OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"))
    
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=openai_embed  # Associate embedding function with the collection
    )
    return collection

def add_documents(collection, documents, metadatas, ids):
    """
    Adds documents to a ChromaDB collection.
    
    :param collection: ChromaDB collection instance.
    :param documents: List of document texts.
    :param metadatas: List of metadata dictionaries.
    :param ids: List of unique IDs for each document.
    """
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

def query_collection(collection, query_text, n_results=5):
    """
    Queries the ChromaDB collection for relevant documents.
    
    :param collection: ChromaDB collection instance.
    :param query_text: The query string.
    :param n_results: Number of results to retrieve.
    :return: Query results containing relevant documents.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    return results