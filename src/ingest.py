import tempfile
import os
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from src.config import (
    QDRANT_URL,
    QDRANT_API_KEY,
    EMBEDDING_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)
from src.qdrant_utils import delete_collection


def load_pdf_documents(uploaded_file) -> list[Document]:
    """
    Takes a Streamlit UploadedFile, extracts text page by page,
    and returns a list of LangChain Document objects with page metadata.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        reader = PdfReader(tmp_path)
        documents = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "page_label": str(i + 1),
                            "source_file": uploaded_file.name,
                        },
                    )
                )
        return documents
    finally:
        os.unlink(tmp_path)


def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)


def ingest_pdf(uploaded_file, collection_name: str) -> QdrantVectorStore:
    """
    Full pipeline: load PDF -> chunk -> embed -> upload to a fresh Qdrant collection.
    """
    delete_collection(collection_name)

    documents = load_pdf_documents(uploaded_file)
    if not documents:
        raise ValueError(
            "No extractable text found in this PDF. It may be a scanned/image-only document."
        )

    chunks = chunk_documents(documents)
    embedding_model = get_embedding_model()

    vector_db = QdrantVectorStore.from_documents(
        chunks,
        embedding=embedding_model,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=collection_name,
    )

    return vector_db