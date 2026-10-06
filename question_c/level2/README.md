# Question C — Level 2: Code it yourself

The manual retriever is in `app/rag.py` and implements:
- document chunking;
- vocabulary construction;
- term frequency;
- inverse document frequency;
- TF-IDF vectors;
- query vectorization;
- cosine similarity with NumPy;
- top-K ranking.

No vector database or retriever library is used for the manual path. The library comparison uses scikit-learn's `TfidfVectorizer` and cosine similarity separately.
