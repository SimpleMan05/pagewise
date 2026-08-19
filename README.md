
# PageWise

*A RAG-based chat app with your documents.*

PageWise is a Retrieval-Augmented Generation (RAG) application that lets you upload a PDF and ask questions about it in plain language. Answers are grounded strictly in the document's actual content, with page-level source attribution so you can verify anything it tells you.


<div align="center">
  <img src="static/logo2.png" alt = "" width="200">
</div>

## How it works

```
PDF Upload
    │
    ▼
Text Extraction (pypdf)
    │
    ▼
Chunking (LangChain RecursiveCharacterTextSplitter)
    │
    ▼
Embedding (HuggingFace sentence-transformers — all-MiniLM-L6-v2, runs locally)
    │
    ▼
Vector Storage (Qdrant Cloud)
    │
    ▼
User Query → Semantic Search (top-k retrieval)
    │
    ▼
Context-Grounded Generation (Groq — Llama-based inference)
    │
    ▼
Answer + Page References
```

Each session gets its own isolated Qdrant collection. When the chat ends, the collection is deleted — no data persists between sessions.

## Tech Stack

- **Frontend**: Streamlit
- **Orchestration**: LangChain
- **Embeddings**: HuggingFace `sentence-transformers` (local, no API cost)
- **Vector Database**: Qdrant Cloud
- **LLM Inference**: Groq (`openai/gpt-oss-20b`)
- **PDF Parsing**: pypdf

## Features

- Upload any PDF and chat with it in natural language
- Answers grounded only in retrieved document context (reduces hallucination)
- Page-level source citations for every answer
- Ephemeral, session-based storage — nothing persists after you leave
- Clean error handling with graceful recovery

## Local Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/pagewise.git
   cd pagewise
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables — copy `.env.example` to `.env` and fill in your keys:
   ```
   GROQ_API_KEY=your_groq_key
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   ```

   - Get a free Groq API key at [console.groq.com](https://console.groq.com)
   - Get a free Qdrant Cloud cluster at [cloud.qdrant.io](https://cloud.qdrant.io)

5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
pagewise/
├── app.py                 # Landing page
├── pages/
│   └── 1_Chat.py            # Chat interface
├── src/
│   ├── config.py             # Env vars + constants
│   ├── ingest.py              # PDF loading, chunking, embedding, upload
│   ├── retrieve.py            # Similarity search + LLM generation
│   ├── qdrant_utils.py         # Collection management
│   └── styles.py               # Custom CSS (moonlit theme)
├── assets/                  # Static images (favicon, etc.)
├── requirements.txt
└── .env.example
```

## Design Notes

- **Why local embeddings?** Eliminates per-query API costs and rate limits for the embedding step — only the final generation call uses a hosted API.
- **Why session-scoped Qdrant collections?** Prevents cross-user data bleed and keeps the app stateless between sessions, matching the intended "ephemeral chat" use case.
- **Chunking**: 1000-character chunks with 400-character overlap, tuned to reduce fragmentation of structured content (e.g., syllabi, lists) across chunk boundaries.

## License

[GNU GENERAL PUBLIC LICENSE](https://github.com/SimpleMan05/pagewise/blob/main/LICENSE)