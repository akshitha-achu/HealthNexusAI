from pathlib import Path
import json
from app.rag import rank_chunks, library_rank_chunks, ask_health_ai

ROOT = Path(__file__).resolve().parents[1]
questions = json.loads((ROOT/'evaluation/questions.json').read_text())
lines = ['# RAG Evaluation Results', '', '| ID | Question | Expected | Top-1 score | Top-1 source | Boundary |', '|---:|---|---|---:|---|---|']
for q in questions:
    retrieved = rank_chunks(q['question'], 3)
    boundary = retrieved[0]['score'] < 0.08
    answer, mode = ask_health_ai(q['question'], retrieved)
    lines.append(f"| {q['id']} | {q['question']} | {'answerable' if q['answerable'] else 'unanswerable'} | {retrieved[0]['score']:.4f} | {retrieved[0]['doc']} | {'yes' if boundary else 'no'} |")
    lines.append('')
    lines.append(f"**Q{q['id']} answer mode:** {mode}")
    lines.append(f"**Answer:** {answer[:700].replace(chr(10),' ')}")
    lines.append('')
(ROOT/'evaluation/evaluation_results.md').write_text('\n'.join(lines), encoding='utf-8')

compare_questions = [questions[0], questions[2], questions[3]]
clines = ['# Manual vs Library Retriever — Top 3', '', '| Question | Manual Top 3 | Library Top 3 | Same set? |', '|---|---|---|---|']
for q in compare_questions:
    m = rank_chunks(q['question'],3)
    l = library_rank_chunks(q['question'],3)
    ms = [x['doc']+':'+str(x['chunk_id']) for x in m]
    ls = [x['doc']+':'+str(x['chunk_id']) for x in l]
    clines.append(f"| {q['question']} | {', '.join(ms)} | {', '.join(ls)} | {'yes' if set(ms)==set(ls) else 'no'} |")
(ROOT/'evaluation/retriever_comparison.md').write_text('\n'.join(clines), encoding='utf-8')
print('Wrote evaluation/evaluation_results.md and evaluation/retriever_comparison.md')
