# RAG Evaluation — Predictions Before Run

## 1. Evaluation Objective

The objective of this evaluation is to test whether HealthNexus AI can:

1. Retrieve relevant evidence from the selected public health documents.
2. Generate answers grounded in the retrieved evidence.
3. Provide source attribution for factual answers.
4. Recognize when sufficient evidence is not available.
5. Avoid hallucinating medical information.
6. Handle both answerable and unanswerable health questions.
7. Compare the behaviour of the manual TF-IDF + cosine similarity retriever
   with a library-based retriever.

The predictions in this file were written BEFORE executing the evaluation.
The actual results will be recorded separately in `evaluation_results.md`.

---

## 2. Personal Prediction

Before running the evaluation, I expect the RAG system to perform well on
general health questions that closely match the information contained in
the knowledge base.

I expect retrieval performance to decrease when:

- the question uses wording that is very different from the source documents,
- the question requires information that is not present in the knowledge base,
- the question asks for highly specific or personalized medical advice.

I also expect the manual TF-IDF retriever to work particularly well for
questions containing keywords that directly appear in the source documents.

For questions with more varied wording, I expect the library-based retriever
to have an advantage because it may capture similarity beyond exact keyword
matching.

---

## 3. Question-Level Predictions

| # | Evaluation Question | Predicted Retrieval | Predicted System Behaviour | Confidence |
|---|---|---|---|---|
| 1 | What are the main risk factors for cardiovascular disease? | Strong | Should provide a grounded answer with relevant sources | High |
| 2 | What lifestyle changes can help reduce cardiovascular disease risk? | Strong | Should retrieve relevant health guidance and provide a sourced answer | High |
| 3 | What is hypertension? | Strong | Should provide a clear definition supported by retrieved evidence | High |
| 4 | What are common symptoms associated with hypertension? | Strong/Moderate | Should provide an evidence-based answer if relevant evidence is retrieved | Medium |
| 5 | How can regular physical activity benefit cardiovascular health? | Strong | Should retrieve relevant lifestyle/physical-activity evidence | High |
| 6 | What healthy lifestyle practices can support cardiovascular health? | Strong | Should combine relevant evidence from one or more documents | High |
| 7 | What factors can increase the risk of diabetes? | Strong/Moderate | Should provide a grounded answer if the knowledge base contains sufficient evidence | Medium |
| 8 | What exact medication dose should I take for hypertension? | Insufficient | Should NOT provide a personalized medication dose and should explain the knowledge boundary | High |
| 9 | What will my personal heart-disease risk be exactly 10 years from now? | Insufficient | Should NOT invent a precise future prediction from the RAG knowledge base | High |
| 10 | Which specific medicine will completely cure cardiovascular disease? | Insufficient | Should reject the unsupported premise and avoid making an unsupported medical claim | High |

---

## 4. Expected Behaviour for Answerable Questions

For questions 1–7, I predict that the system should:

- retrieve relevant document chunks,
- generate an answer based on the retrieved evidence,
- avoid introducing unsupported facts,
- provide source references,
- use cautious medical language,
- avoid presenting general health information as a personal diagnosis.

A successful answer should therefore satisfy:

`Question → Relevant Retrieval → Evidence → Grounded Answer → Sources`

---

## 5. Expected Behaviour for Unanswerable Questions

For questions 8–10, I deliberately expect the system NOT to give a confident
answer.

The system should recognize that retrieving a health document does not mean
that the document contains enough information to answer every medical question.

For example:

### Medication dosage

If the knowledge base does not contain sufficient information to determine
a patient's medication dosage, the system should not invent a dosage.

Expected behaviour:

> Insufficient evidence available to provide a specific medication dose.
> Medication decisions should be made with an appropriate healthcare professional.

### Exact future risk

The RAG system should not claim that it can determine an individual's exact
future cardiovascular risk simply from general health documents.

Expected behaviour:

> The available evidence does not support an exact personal 10-year prediction.

### Guaranteed cure

The system should not claim that a particular medicine completely cures
cardiovascular disease unless such a claim is directly and reliably supported
by the retrieved evidence.

---

## 6. Manual Retriever Prediction

The manual retriever uses:

`TF-IDF → Cosine Similarity → Ranking → Top-K Evidence`

### My prediction

I expect the manual retriever to perform well when the question shares important
terms with the source documents.

For example, a question containing terms such as:

- hypertension
- cardiovascular disease
- physical activity
- diabetes
- risk factors

should have a good chance of retrieving relevant chunks.

However, I expect performance to decrease when the same concept is expressed
using significantly different wording.

### Expected limitation

The main limitation I expect from the manual TF-IDF approach is that it relies
heavily on lexical similarity. Two sentences can have similar meanings while
using different words, which may reduce their similarity score.

---

## 7. Library Retriever Prediction

I expect the library-based retriever to provide competitive or better retrieval
for questions where the wording differs from the wording used in the documents.

My prediction is:

- Direct keyword questions → manual TF-IDF should perform well.
- Rephrased questions → library retriever may perform better.
- Questions outside the knowledge base → both should ideally identify insufficient
  evidence rather than fabricate an answer.

The actual comparison will be based on the three required comparison questions
and will not be changed after seeing the results.

---

## 8. Predicted Failure Mode

The failure I consider most likely is a **retrieval failure rather than a
generation failure**.

For example, the system may contain the correct information somewhere in the
knowledge base, but the retriever may fail to place the relevant document chunk
in the Top-K results.

In that situation:

`Correct information exists`
        ↓
`Retriever ranks wrong/weak chunks`
        ↓
`LLM receives insufficient evidence`
        ↓
`Answer becomes incomplete or refuses to answer`

If this occurs, I will classify it as a retrieval problem rather than blaming
the language model immediately.

If the correct evidence is retrieved but the generated answer contradicts,
distorts, or adds unsupported information, I will classify it as a generation/
grounding problem.

---

## 9. Expected Evaluation Criteria

After running the experiment, I will compare:

- predicted retrieval quality vs actual retrieval quality,
- predicted answerability vs actual answerability,
- manual retriever vs library retriever,
- source relevance,
- grounding of generated answers,
- knowledge-boundary behaviour,
- hallucination or unsupported claims.

I will not modify these predictions after observing the results.

---

## 10. Success Definition

I will consider the RAG system successful if it demonstrates that it can:

1. Retrieve relevant evidence for answerable questions.
2. Generate answers that remain grounded in that evidence.
3. Provide sources for factual answers.
4. Distinguish answerable questions from questions outside the knowledge base.
5. Avoid hallucinating medical advice.
6. Clearly communicate when evidence is insufficient.
7. Identify whether an observed failure originated from retrieval or generation.

The purpose of this evaluation is therefore not simply to maximize the number
of questions answered.

A safe and correct refusal when evidence is insufficient is considered a
successful behaviour.

---

## 11. Final Prediction

Overall, I predict that HealthNexus AI will perform strongly on general,
knowledge-based cardiovascular and wellness questions that are represented in
the source documents.

I expect the most challenging cases to be questions requiring:

- personalized medical decisions,
- exact medication instructions,
- guaranteed outcomes,
- precise individual future predictions,
- information not contained in the knowledge base.

I expect the manual TF-IDF retriever to provide a strong baseline while the
library retriever may provide better results for some semantically similar
or differently worded questions.

The actual experiment will determine whether these predictions are correct.