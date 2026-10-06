# Question C – Failure Analysis

The assignment requires one weak or incorrect answer and evidence showing whether the problem was caused by retrieval or generation.

## Case Selected

- **Question ID:** 4
- **Question:** What are the core principles of a healthy diet?
- **Expected:** A concise answer explaining the core principles of a healthy diet using the trusted evidence.
- **Top-1 retrieved source:** `who_healthy_diet.md`
- **Top-1 retrieval score:** 0.3331

## What HealthNexus Answered

The answer correctly started with:

- Adequacy
- Balance
- Moderation
- Variety

However, the answer then introduced several unrelated topics, including physical activity, sleep, anxiety, hypertension, cardiovascular disease, and hypertension risk factors.

The answer also became incomplete near the end.

## Diagnosis

### Retrieval failure?

**No.**

The Top-1 retrieved document was:

`who_healthy_diet.md`

This document is directly relevant to the question about the principles of a healthy diet.

Therefore, the retrieval component successfully identified an appropriate source.

### LLM failure?

**Yes.**

The main weakness occurred during answer generation.

Although the language model extracted the correct core principles from the retrieved document, it generated additional information that was not directly relevant to the user's question.

The response therefore became less focused and less precise than expected.

## Evidence

The answer correctly identified:

- adequacy
- balance
- moderation
- variety

However, it then moved into unrelated information about:

- physical activity
- sleep
- anxiety
- hypertension
- cardiovascular disease
- hypertension risk factors

This indicates that the model did not sufficiently restrict its generation to the question being asked.

## Root Cause

The likely root cause is insufficient generation control.

The retriever supplied a relevant document, but the language model appears to have combined multiple pieces of retrieved evidence instead of selecting only the information necessary to answer the question.

This demonstrates that a RAG system can retrieve relevant evidence successfully while still producing an unfocused answer.

## Fix I Would Make

I would improve the generation stage by enforcing the following rules:

1. Answer only the question asked by the user.
2. Use only information directly relevant to the question from the retrieved evidence.
3. Do not introduce unrelated topics from other parts of the retrieved context.
4. Prefer concise answers for simple factual questions.
5. Preserve the meaning of the source without adding unsupported claims.
6. Include the source used for the answer.
7. Add an answer-relevance check after generation to identify unrelated content.

I would also reduce the amount of retrieved context supplied to the language model when a question is narrow and factual.

## Key Learning

This failure demonstrates that RAG has two separate stages:

**Retrieval → Generation**

In this case:

**Retrieval worked:**  
The system retrieved `who_healthy_diet.md`, which is relevant to the question.

**Generation was weak:**  
The LLM produced a partially correct answer but added unrelated health information.

Therefore, improving RAG quality requires evaluating both retrieval relevance and generation faithfulness/relevance.