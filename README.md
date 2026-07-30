                 Upload Logs
                      │
                      ▼
                 FastAPI Backend
                      │
                      ▼
                 Chunk Logs
                      │
                      ▼
           Create Embeddings
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
      Store in FAISS         Build BM25 Index
          │                       │
          └───────────┬───────────┘
                      │
                 User Question
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
     Semantic Search        Keyword Search
        (FAISS)                 (BM25)
          │                       │
          └───────────┬───────────┘
                      ▼
             Hybrid Retrieval
                      │
                      ▼
           Remove Duplicates
                      │
                      ▼
         CrossEncoder Reranker
                      │
                 Top 5 Chunks
                      │
                      ▼
             Prompt Construction
                      │
                      ▼
             Groq Llama-3.3-70B
                      │
                      ▼
               JSON Response
                      │
                      ▼
                 Frontend UI