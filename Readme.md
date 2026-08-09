My first RAG project!

this project documents a question and answering system.
it starts from a simple "what is the refund policy" question

## `01-in-memory-rag/` — query-memory.py is my first attempt at building a RAG pipeline
1. used llamaindex to store policy data in memory
2. cohere for creation and returning of embeddings
3. my questions were hardcoded strings for Claude to handle query and return answer to user

## `02-graph-rag/` — i then decided to move to graphRAG
1. switched orchestration from LlamaIndex to Langchain, data store to Neo4j
2. updated query logic. script will use vector similarity search to find top chunks, then invoke graph traversal on those chunks. graph traversal goes beyond top k chunks to find connected entities and relationships
3. Query is still used for Claude in order to get to answer
4. added RAGAS evaluation (`eval-ragas.py`) to score faithfulness/answer relevancy of generated answers

Questions
1. Simple, already have answer to: what is the return policy if my item is bought last year
2. Vague, no direct answer:  what is the return policy if my item is bought in a different country

## `03-observability-pipeline/` — then turned the eval script into an analytical eval pipeline
1. `instrumented_pipeline.py` wraps the stage 2 query pipeline to capture latency (retrieval vs. generation), token usage, and a Langfuse trace per run — without modifying the stage 2 files themselves
2. `clickhouse_logger.py` batches every query run (question, retrieval method, retrieved chunks, answer, RAGAS scores, latency, token cost) into a ClickHouse `query_runs` table, so it's queryable ("avg faithfulness by retrieval method", "which questions tank context precision") instead of just printed once and discarded
3. `eval_ragas_clickhouse.py` is the entry point — runs RAGAS same as stage 2, then logs every row to both ClickHouse (SQL analytics) and Langfuse (trace visualization + PASS/FAIL-style scoring)

## How to run
Everything shares one `venv`/`requirements.txt` and one root-level `.env` (Neo4j, Anthropic, Cohere, ClickHouse, Langfuse credentials). **Always run scripts from the repo root**, not from inside a stage folder — a couple of scripts reference `data/nintendo.pdf` with a path relative to the working directory.

```bash
source venv/bin/activate
python 01-in-memory-rag/query-memory.py
python 02-graph-rag/document-ingestion-neo4j.py   # run once to populate Neo4j
python 02-graph-rag/query_neo4j.py
python 02-graph-rag/eval-ragas.py
python 03-observability-pipeline/eval_ragas_clickhouse.py
```

==========
Todos
1. how to handle multiple input documents
2. i dont know what document types can be handled
