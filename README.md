# HealthNexus AI

HealthNexus AI is a trusted health-information assistant and health-risk application developed for the Technical Assignment: AI for Personal Health and Wellness.

The project focuses on two assignment questions:

- Question B – Turn a model into a usable app
- Question C – Build a trusted health-information assistant

---

## Personal Seed

- USN suffix: `0400`
- Numeric Python seed: `400`

The seed `400` is used for the model split and model random state so that the results are reproducible and specific to my assignment seed.

---

# Question B – Turn a Model into a Usable App

HealthNexus AI serves trained health-risk prediction models through a FastAPI application.

The application provides:

- Health-risk prediction through an API
- Input validation
- Logistic Regression model
- Random Forest model
- SQLite-based application support
- Automated testing using Pytest
- API documentation through Swagger UI

The trained models are stored in the `models/` directory.

---

# Question C – Trusted Health-Information Assistant

HealthNexus AI also provides a Retrieval-Augmented Generation (RAG) based health-information assistant.

The assistant:

1. Receives a health-related question.
2. Searches trusted public-health documents.
3. Splits documents into chunks.
4. Creates TF-IDF representations.
5. Ranks document chunks using cosine similarity.
6. Retrieves the top relevant evidence.
7. Sends the retrieved evidence to the local TinyLlama model through Ollama.
8. Generates an evidence-based answer.
9. Returns the source documents used.
10. Applies a knowledge boundary for questions that require personalized medical advice.

The assistant is designed to avoid making diagnoses, prescribing medication, or inventing medical information.

---

# Trusted Sources

The RAG knowledge base contains public-health information from trusted sources such as:

- CDC
- WHO

Example topics include:

- Heart disease risk factors
- High blood pressure
- Physical activity
- Healthy diet
- Hypertension

---

# Local LLM

The project uses:

- Ollama
- TinyLlama

The local model is:

```text
tinyllama:latest