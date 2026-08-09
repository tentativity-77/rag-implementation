"""
RAGAS evaluation for the hybrid Neo4j RAG pipeline, logged to ClickHouse.

Parallel to eval-ragas.py -- same questions, same metrics -- but also
captures latency/token usage per run (via instrumented_pipeline.py) and
persists every row to ClickHouse instead of only printing to console.
"""

import uuid
from datetime import datetime, timezone

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import Faithfulness, ResponseRelevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from query_neo4j import llm, embeddings
from instrumented_pipeline import run_instrumented_query
from clickhouse_logger import log_query_runs, estimate_cost_usd

TEST_QUESTIONS = [
    "What is the return policy if my item was bought in a different country?",
    "Can I return an item after 30 days?",
    "Do I need the original packaging to return a product?",
]

EVAL_RUN_ID = uuid.uuid4()

run_results = {}
rows = []
for q in TEST_QUESTIONS:
    result = run_instrumented_query(q)
    run_results[q] = result
    rows.append({
        "question": q,
        "answer": result.answer,
        "contexts": result.chunks + result.graph_facts,
    })
    print(f"done: {q}")

dataset = Dataset.from_list(rows)

ragas_llm = LangchainLLMWrapper(llm)
ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)

result = evaluate(
    dataset,
    metrics=[
        Faithfulness(),
        ResponseRelevancy(),
    ],
    llm=ragas_llm,
    embeddings=ragas_embeddings,
)

print("\n=== RAGAS RESULTS ===")
print(result)

df = result.to_pandas()
print("\n=== PER-QUESTION BREAKDOWN ===")
print(df[["user_input", "faithfulness", "answer_relevancy"]].to_string(index=False))

clickhouse_rows = []
for _, row in df.iterrows():
    q = row["user_input"]
    r = run_results[q]
    clickhouse_rows.append({
        "run_id": str(uuid.uuid4()),
        "eval_run_id": str(EVAL_RUN_ID),
        "timestamp": datetime.now(timezone.utc),
        "question": q,
        "retrieval_method": r.retrieval_method,
        "retrieved_chunks": r.chunks,
        "graph_facts": r.graph_facts,
        "answer": r.answer,
        "faithfulness": row.get("faithfulness"),
        "answer_relevancy": row.get("answer_relevancy"),
        "context_precision": row.get("context_precision"),
        "latency_retrieval_ms": r.latency_retrieval_ms,
        "latency_generation_ms": r.latency_generation_ms,
        "latency_total_ms": r.latency_total_ms,
        "input_tokens": r.input_tokens,
        "output_tokens": r.output_tokens,
        "estimated_cost_usd": estimate_cost_usd(r.llm_model, r.input_tokens, r.output_tokens),
        "llm_model": r.llm_model,
        "embedding_model": r.embedding_model,
    })

log_query_runs(clickhouse_rows)
print(f"\nLogged {len(clickhouse_rows)} rows to ClickHouse (eval_run_id={EVAL_RUN_ID})")
