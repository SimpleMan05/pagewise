import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys / Connection Info ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

# --- Model Config ---
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL_NAME = "openai/gpt-oss-20b"

# --- Chunking Config ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 400

# --- Retrieval Config ---
TOP_K = 8


# --- Basic sanity check on startup ---
def validate_config():
    missing = []
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if not QDRANT_URL:
        missing.append("QDRANT_URL")
    if not QDRANT_API_KEY:
        missing.append("QDRANT_API_KEY")
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Check your .env file."
        )