import time
from dataclasses import dataclass

from langchain_core.callbacks import get_usage_metadata_callback

import query_neo4j  # importing this fires its unguarded test call once (query_neo4j.py:125-128)

RETRIEVAL_METHOD = "hybrid_vector_graph"
LLM_MODEL_NAME = "claude-sonnet-4-6"
EMBEDDING_MODEL_NAME = "embed-english-v3.0"

_original_hybrid_retrieve = query_neo4j.hybrid_retrieve


@dataclass
class QueryRunResult:
    question: str
    answer: str
    chunks: list[str]
    graph_facts: list[str]
    retrieval_method: str
    latency_retrieval_ms: float | None
    latency_generation_ms: float | None
    latency_total_ms: float
    input_tokens: int | None
    output_tokens: int | None
    llm_model: str
    embedding_model: str


def run_instrumented_query(question: str) -> QueryRunResult:
    capture = {}

    def _timed_hybrid_retrieve(q, k=3):
        t0 = time.perf_counter()
        chunks, facts = _original_hybrid_retrieve(q, k=k)
        capture["latency_retrieval_ms"] = (time.perf_counter() - t0) * 1000
        capture["chunks"], capture["graph_facts"] = chunks, facts
        return chunks, facts

    query_neo4j.hybrid_retrieve = _timed_hybrid_retrieve
    try:
        t_start = time.perf_counter()
        with get_usage_metadata_callback() as cb:
            answer, _ = query_neo4j.answer_question(question)
        latency_total_ms = (time.perf_counter() - t_start) * 1000
    finally:
        query_neo4j.hybrid_retrieve = _original_hybrid_retrieve

    usage = cb.usage_metadata.get(LLM_MODEL_NAME, {})
    retrieval_ms = capture.get("latency_retrieval_ms")

    return QueryRunResult(
        question=question,
        answer=answer,
        chunks=capture.get("chunks", []),
        graph_facts=capture.get("graph_facts", []),
        retrieval_method=RETRIEVAL_METHOD,
        latency_retrieval_ms=retrieval_ms,
        latency_generation_ms=(latency_total_ms - retrieval_ms) if retrieval_ms is not None else None,
        latency_total_ms=latency_total_ms,
        input_tokens=usage.get("input_tokens"),
        output_tokens=usage.get("output_tokens"),
        llm_model=LLM_MODEL_NAME,
        embedding_model=EMBEDDING_MODEL_NAME,
    )
