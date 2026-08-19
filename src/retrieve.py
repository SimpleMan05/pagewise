import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_qdrant import QdrantVectorStore

from src.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    LLM_MODEL_NAME,
    TOP_K,
)
from src.ingest import get_embedding_model


def connect_to_collection(collection_name: str) -> QdrantVectorStore:
    """Connect to an existing Qdrant collection for querying."""
    embedding_model = get_embedding_model()
    return QdrantVectorStore.from_existing_collection(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=collection_name,
        embedding=embedding_model,
    )


def build_context(search_results) -> str:
    return "\n\n\n".join(
        [
            f"Page Content: {result.page_content}\n"
            f"Page Number: {result.metadata.get('page_label', 'unknown')}\n"
            f"Source: {result.metadata.get('source_file', 'unknown')}"
            for result in search_results
        ]
    )


def get_answer(vector_db: QdrantVectorStore, user_query: str) -> str:
    """
    Full retrieve + generate step: searches the vector DB,
    builds a grounded prompt, and returns the LLM's answer.
    """
    search_results = vector_db.similarity_search(query=user_query, k=TOP_K)

    if not search_results:
        return "I couldn't find anything relevant to that in the document."

    context = build_context(search_results)

    system_prompt = f"""You are a helpful assistant that answers questions based only on the context provided below, which was retrieved from a PDF document.

Rules:
- Only answer using the given context. If the answer isn't in the context, say you don't know — don't make things up.
- When relevant, point the user to the page number(s) where they can read more.

Context:
{context}
"""

    llm = ChatGroq(model=LLM_MODEL_NAME,
                   api_key=os.environ["GROQ_API_KEY"])

    response = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query),
        ]
    )

    return response.content