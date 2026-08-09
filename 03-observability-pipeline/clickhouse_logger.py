import os

import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

_client = None

_COLUMNS = [
    "run_id", "eval_run_id", "timestamp", "question", "retrieval_method",
    "retrieved_chunks", "graph_facts", "answer",
    "faithfulness", "answer_relevancy", "context_precision",
    "latency_retrieval_ms", "latency_generation_ms", "latency_total_ms",
    "input_tokens", "output_tokens", "estimated_cost_usd",
    "llm_model", "embedding_model",
]

# TODO: verify current Anthropic pricing before relying on this for anything
# beyond rough demo numbers -- pricing changes over time. Check
# https://www.anthropic.com/pricing at execution time.
_PRICE_PER_MTOK_USD = {
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
}


def get_client():
    global _client
    if _client is None:
        _client = clickhouse_connect.get_client(
            host=os.environ["CLICKHOUSE_HOST"],
            port=int(os.getenv("CLICKHOUSE_PORT", 8443)),
            username=os.environ["CLICKHOUSE_USER"],
            password=os.environ["CLICKHOUSE_PASSWORD"],
            database=os.getenv("CLICKHOUSE_DATABASE", "default"),
            secure=True,
        )
    return _client


def log_query_runs(rows: list[dict]) -> None:
    """Batched insert -- call once per eval run, not once per row."""
    if not rows:
        return
    client = get_client()
    data = [[row.get(col) for col in _COLUMNS] for row in rows]
    client.insert("query_runs", data, column_names=_COLUMNS)


def estimate_cost_usd(model: str, input_tokens: int | None, output_tokens: int | None) -> float | None:
    if input_tokens is None or output_tokens is None:
        return None
    prices = _PRICE_PER_MTOK_USD.get(model)
    if not prices:
        return None
    return (input_tokens / 1_000_000) * prices["input"] + (output_tokens / 1_000_000) * prices["output"]
