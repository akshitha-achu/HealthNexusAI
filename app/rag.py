from pathlib import Path
import math
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity
from .config import DOCS_PATH


def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_documents(chunk_words=120, overlap=25):
    chunks = []
    for path in sorted(DOCS_PATH.glob('*.md')):
        text = path.read_text(encoding='utf-8')
        words = clean_text(text).split()
        start = 0
        idx = 0
        while start < len(words):
            end = min(len(words), start + chunk_words)
            chunk = ' '.join(words[start:end])
            chunks.append({'doc': path.name, 'chunk_id': idx, 'text': chunk})
            if end == len(words):
                break
            start = max(end - overlap, start + 1)
            idx += 1
    return chunks


def tokenize(text):
    return re.findall(r'[a-z0-9]+', text.lower())


def build_vocabulary(chunks):
    vocab = {}
    for c in chunks:
        for token in set(tokenize(c['text'])):
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab


def calculate_tf(tokens, vocab):
    vec = np.zeros(len(vocab), dtype=float)
    if not tokens:
        return vec
    for token in tokens:
        if token in vocab:
            vec[vocab[token]] += 1
    return vec / len(tokens)


def calculate_idf(chunks, vocab):
    n = len(chunks)
    df = np.zeros(len(vocab), dtype=float)
    for c in chunks:
        for token in set(tokenize(c['text'])):
            if token in vocab:
                df[vocab[token]] += 1
    return np.log((1 + n) / (1 + df)) + 1


def calculate_tfidf(chunks, vocab, idf):
    return np.vstack([calculate_tf(tokenize(c['text']), vocab) * idf for c in chunks])


def vectorize_query(query, vocab, idf):
    return calculate_tf(tokenize(query), vocab) * idf


def cosine_similarity(a, b):
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def rank_chunks(query, top_k=3):
    chunks = chunk_documents()
    vocab = build_vocabulary(chunks)
    idf = calculate_idf(chunks, vocab)
    matrix = calculate_tfidf(chunks, vocab, idf)
    q = vectorize_query(query, vocab, idf)
    scores = [cosine_similarity(q, row) for row in matrix]
    order = np.argsort(scores)[::-1][:top_k]
    return [{**chunks[i], 'score': round(scores[i], 6)} for i in order]


def library_rank_chunks(query, top_k=3):
    chunks = chunk_documents()
    texts = [c['text'] for c in chunks]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(texts)
    q = vectorizer.transform([query])
    scores = sklearn_cosine_similarity(q, matrix).ravel()
    order = np.argsort(scores)[::-1][:top_k]
    return [{**chunks[i], 'score': round(float(scores[i]), 6)} for i in order]

def answer_without_llm(query, retrieved):
    unsafe_personal = any(
        term in query.lower()
        for term in [
            'exact medication',
            'medication dose',
            'medication',
            'what dose',
            'my personal',
            'for me',
            'what should i take',
            'treatment plan',
            'prescribe'
        ]
    )

    if unsafe_personal or not retrieved or retrieved[0]['score'] < 0.08:
        return (
            'I do not have enough evidence in the trusted documents to answer '
            'that question reliably. Please consult a qualified healthcare '
            'professional for personalized guidance.'
        )

    snippets = []

    for r in retrieved[:2]:
        text = r['text']
        snippets.append(text[:420])

    return (
        'Based on the retrieved public-health evidence:\n\n'
        + '\n\n'.join(snippets)
        + '\n\nThis is general information, not a diagnosis or personalized medical advice.'
    )
def ask_health_ai(query, retrieved):
    from .config import OPENAI_API_KEY, OPENAI_MODEL
    import json
    import urllib.request
    import urllib.error

    # Keep personalized medical requests behind the knowledge boundary.
    unsafe_personal = any(
        term in query.lower()
        for term in [
            'exact medication',
            'medication dose',
            'medication',
            'what dose',
            'my personal',
            'for me',
            'what should i take',
            'treatment plan',
            'prescribe'
        ]
    )

    if unsafe_personal:
        return answer_without_llm(query, retrieved), 'knowledge boundary'

    if not retrieved or retrieved[0]['score'] < 0.08:
        return answer_without_llm(query, retrieved), 'knowledge boundary'

    evidence = '\n\n'.join(
        [f"SOURCE: {r['doc']}\n{r['text']}" for r in retrieved]
    )

    system = (
        'You are HealthNexus AI, a trusted health-information assistant. '
        'Answer ONLY using the supplied public-health evidence. '
        'Do not diagnose, prescribe medication, invent facts, or make unsupported '
        'personal medical predictions. If the evidence is insufficient, clearly '
        'say that the available evidence is insufficient. '
        'Use cautious language. Mention the source documents used. '
        'Keep the answer concise and easy to understand.'
    )

    user_prompt = (
        f"Question: {query}\n\n"
        f"Retrieved public-health evidence:\n{evidence}\n\n"
        "Answer the question using only this evidence."
    )

    # ---------------------------------------------------------
    # 1. Try OpenAI when an API key is configured
    # ---------------------------------------------------------
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=OPENAI_API_KEY)

            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                temperature=0.1,
                messages=[
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': user_prompt},
                ],
            )

            return response.choices[0].message.content, 'llm-openai'

        except Exception:
            pass

    # ---------------------------------------------------------
    # 2. Use local Ollama + TinyLlama when OpenAI is unavailable
    # ---------------------------------------------------------
    try:
        payload = {
            "model": "tinyllama:latest",
            "messages": [
                {
                    "role": "system",
                    "content": system
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }

        request = urllib.request.Request(
            "http://localhost:11434/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result.get("message", {}).get("content", "").strip()

        if answer:
            return answer, 'llm-ollama-tinyllama'

    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception):
        pass

    # ---------------------------------------------------------
    # 3. Safe fallback if both LLM options are unavailable
    # ---------------------------------------------------------
    return answer_without_llm(
        query,
        retrieved
    ), 'evidence-only fallback (LLM unavailable)'