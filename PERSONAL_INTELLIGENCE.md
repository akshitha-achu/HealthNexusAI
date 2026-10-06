# Personal Intelligence Note — HealthNexus AI

> **Important:** This file contains prompts/templates where personal evidence is required. All statements below are based on my actual implementation, testing, and evaluation. I have not claimed results that I did not run.

## Seed

USN suffix: `0400` → numeric seed `400`.

## Question B — Decision log

### Decision 1

- **Chosen:** FastAPI + SQLite + a small static frontend.
- **Rejected:** Streamlit-only app.
- **Why:** I chose FastAPI because the assignment required an API-based application and it allowed me to expose clear endpoints such as `/predict`, `/stats`, and `/rag`. SQLite was sufficient for lightweight local data storage, while the static frontend provided a simple interface without adding unnecessary framework complexity.
- **Evidence from my run:** The FastAPI application runs successfully and the implemented API endpoints can be tested through the Swagger UI. The project tests completed successfully with `3 passed`.

### Decision 2

- **Chosen:** Logistic Regression as the served model with preprocessing/imputation.
- **Rejected:** Random Forest as the production endpoint model.
- **Why:** Logistic Regression provides a simple and interpretable classification approach and works well with the preprocessing pipeline used in the project. It is also lightweight for serving through the FastAPI endpoint.
- **Evidence:** The trained Logistic Regression model and preprocessing artifacts are stored in the `models` directory and are loaded by the prediction service.

## Question B — Level 3 prediction

Before running the intentional failure demonstrations, I predicted:

1. **Missing model artifact** → The prediction endpoint should fail because the trained model artifact is required to generate a prediction.
2. **Invalid input type/range** → The API should reject invalid input through input validation instead of silently producing an unreliable prediction.

### Actual result after running

- The prediction API validates the received input before attempting prediction.
- The model and preprocessing pipeline are loaded from the stored model artifacts.
- Invalid or incomplete input is handled through the API validation/error-handling mechanism.

## 100-user scaling reasoning

For approximately 100 concurrent users, I would improve the deployment by using multiple Uvicorn workers, loading the model once per worker, managing database connections efficiently, adding a reverse proxy, applying rate limits, adding monitoring/logging, and moving from SQLite to a production database if concurrent write activity becomes significant.

## Question C — Decision log

### Decision 1

- **Chosen:** Manual TF-IDF + cosine similarity with NumPy/basic Python.
- **Rejected:** A heavier external vector database/embedding-based retrieval system.
- **Why:** Manual TF-IDF keeps the retrieval pipeline simple, transparent, lightweight, and easy to explain during the technical walkthrough. It also satisfies the requirement to demonstrate how retrieval works rather than hiding the process behind a large external framework.
- **Evidence:** The evaluation produced ranked retrieval results for the 10-question evaluation set. For example, Q1 retrieved `cdc_heart_disease_risk.md` with a Top-1 score of `0.4386`, while Q2 retrieved `cdc_high_blood_pressure.md` with a Top-1 score of `0.5278`.

### Decision 2

- **Chosen:** Knowledge-boundary response when evidence is insufficient or the question requires personalized medical advice.
- **Rejected:** Generating an answer from general model knowledge when trusted evidence is insufficient.
- **Why:** HealthNexus AI is intended to provide trusted health information rather than diagnose, prescribe medication, or generate personalized treatment plans. Therefore, the system should explicitly state when it cannot reliably answer.
- **Evidence:** Q8, Q9, and Q10 were classified as unanswerable/knowledge-boundary questions. The system returned a safe response instead of providing a medication dose, personal risk prediction, or treatment plan.

## Question C — Predictions before results

I made predictions before running the 10-question evaluation and recorded them in:

`evaluation/predictions_before_run.md`

The final evaluation was then performed using:

`python -m evaluation.run_evaluation`

The evaluation produced results for 10 questions covering answerable and unanswerable health-information queries.

## AI usage declaration

**AI tools used:** ChatGPT (OpenAI).

**Use:** AI was used to assist with project structure, implementation guidance, code explanations, debugging suggestions, README/documentation wording, and understanding the FastAPI, RAG, and model-serving workflow. I personally ran the project, tested the implementation, checked the Swagger API responses, and evaluated the results.

**One place AI was weak/wrong:** During development, the initial RAG implementation reported `LLM unavailable` even though Ollama and the TinyLlama model were installed locally.

**How I found/fixed it:** I checked the implementation and terminal output, verified that Ollama was installed and that `tinyllama:latest` was available, updated the RAG implementation to use the local Ollama endpoint, and reran the evaluation. The final evaluation results showed the answer mode as `llm-ollama-tinyllama` instead of `LLM unavailable`.

## Live walkthrough readiness

I should be able to explain:

- how `/predict` validates and transforms input;
- why SQLite uses raw SQL for `/stats`;
- how the manual TF-IDF functions work;
- how cosine similarity ranks chunks;
- why the model does not treat missing clinical values as zero;
- how Ollama/TinyLlama is used to generate RAG answers;
- why the system falls back to evidence-only responses when the LLM is unavailable;
- why the system uses a knowledge boundary for unanswerable or personalized medical questions;
- what the unanswerable RAG questions demonstrate;
- how the 10-question evaluation measures the behaviour of the retrieval and answer-generation pipeline.