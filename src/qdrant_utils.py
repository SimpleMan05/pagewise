from qdrant_client import QdrantClient
from src.config import QDRANT_URL, QDRANT_API_KEY


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


def delete_collection(collection_name: str) -> bool:
    """Delete a collection if it exists. Returns True if deleted, False if it didn't exist."""
    client = get_qdrant_client()
    if client.collection_exists(collection_name=collection_name):
        client.delete_collection(collection_name=collection_name)
        return True
    return False


def collection_exists(collection_name: str) -> bool:
    client = get_qdrant_client()
    return client.collection_exists(collection_name=collection_name)