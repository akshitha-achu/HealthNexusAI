# Question C — Level 1: Build

Six public health source documents are stored in `data/health_docs/`. `POST /rag` retrieves the top three chunks and then calls an optional OpenAI-compatible LLM. If no API key is available, the app uses an evidence-only fallback instead of inventing an answer.
