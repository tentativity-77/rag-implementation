"""
RAGAS evaluation for the hybrid Neo4j RAG pipeline.

Starts reference-free: Faithfulness + AnswerRelevancy only need
{question, answer, contexts} -- no ground_truth required.

Once you have reference answers, add "ground_truth" to each row and include
ContextPrecision in the metrics list (see the commented block at the bottom).
"""

import os
from dotenv import load_dotenv
from datasets import Dataset

from ragas import evaluate
from ragas.metrics import Faithfulness, ResponseRelevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# Reuse the exact same llm/embeddings objects your pipeline already uses,
# so RAGAS's judgments are self-consistent with what generated the answers.
from query_neo4j import llm, embeddings, answer_question

load_dotenv()

# ---------------------------------------------------------------------------
# 1. Test questions
#    Swap these for real questions from your actual use case / logs.
# ---------------------------------------------------------------------------

TEST_QUESTIONS = [
    "What is the return policy if my item was bought in a different country?",
    "Can I return an item after 30 days?",
    "Do I need the original packaging to return a product?",
]

# ---------------------------------------------------------------------------
# 2. Run the pipeline on each question, collect answer + contexts
# ---------------------------------------------------------------------------

rows = []
for q in TEST_QUESTIONS:
    answer, contexts = answer_question(q)
    rows.append({
        "question": q,
        "answer": answer,
        "contexts": contexts,  # RAGAS expects a list of strings per row
    })
    print(f"done: {q}")

dataset = Dataset.from_list(rows)

# ---------------------------------------------------------------------------
# 3. Wrap your existing Claude + Cohere objects for RAGAS to use as judge
# ---------------------------------------------------------------------------

ragas_llm = LangchainLLMWrapper(llm)
ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)

# ---------------------------------------------------------------------------
# 4. Run evaluation (reference-free metrics only, for now)
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Once you have ground-truth answers, this is what adding ContextPrecision
# looks like -- uncomment and fill in "ground_truth" per row above:
#
# from ragas.metrics import LLMContextPrecisionWithReference
#
# rows = [
#     {
#         "question": "...",
#         "answer": "...",
#         "contexts": [...],
#         "ground_truth": "the reference answer you'd expect",
#     },
#     ...
# ]
#
# result = evaluate(
#     dataset,
#     metrics=[Faithfulness(), ResponseRelevancy(), LLMContextPrecisionWithReference()],
#     llm=ragas_llm,
#     embeddings=ragas_embeddings,
# )
# ---------------------------------------------------------------------------