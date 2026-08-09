import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_cohere import CohereEmbeddings
from langchain_neo4j import Neo4jVector, Neo4jGraph

load_dotenv()

embeddings = CohereEmbeddings(model="embed-english-v3.0")  # match whatever model you used originally
llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)

# 1. Build a vector index over the chunks Neo4j already has
#    (from_existing_graph reads text off your existing Document/chunk nodes)
vector_store = Neo4jVector.from_existing_graph(
    embedding=embeddings,
    url=os.environ["NEO4J_URI"],
    username=os.environ["NEO4J_USERNAME"],
    password=os.environ["NEO4J_PASSWORD"],
    index_name="chunk_vector_index",
    node_label="Document",          # the chunk/source nodes created by include_source=True
    text_node_properties=["text"],  # property holding the chunk text
    embedding_node_property="embedding",
)

graph = Neo4jGraph(
    url=os.environ["NEO4J_URI"],
    username=os.environ["NEO4J_USERNAME"],
    password=os.environ["NEO4J_PASSWORD"],
)

def graph_traverse_from_chunk(chunk_id: str, hops: int = 1):
    query = f"""
    MATCH (d:Document {{id: $chunk_id}})-[:MENTIONS]->(e)
    MATCH path = (e)-[*1..{hops}]-(connected)
    RETURN DISTINCT e.id AS entity, type(relationships(path)[0]) AS relationship, connected.id AS connected_entity
    LIMIT 15
    """
    print("=== EXACT QUERY ===")
    print(query)
    print("=== PARAMS ===")
    print({"chunk_id": chunk_id})
    return graph.query(query, params={"chunk_id": chunk_id})


#this function calls graph_traverse_from_chunk
# it will do vector search first and put the relevant chunks in vector_results
# and then put it intp graph_facts
def hybrid_retrieve(question: str, k: int = 3):
    # Vector search: find top-k relevant chunks
    vector_results = vector_store.similarity_search_with_score(question, k=k)

    chunk_texts = []
    graph_facts = []

    for doc, score in vector_results:
        chunk_texts.append(doc.page_content)
        chunk_id = doc.metadata.get("id")
        if chunk_id:
            facts = graph_traverse_from_chunk(chunk_id)
            for f in facts:
                graph_facts.append(f"{f['entity']} --{f['relationship']}--> {f['connected_entity']}")

    return chunk_texts, list(set(graph_facts))


# #this function calls hybrid_retrieve, which calls graph_traverse_from_chunk
# def answer_question(question: str):
#     chunks, facts = hybrid_retrieve(question)

#     context = "Relevant text excerpts:\n" + "\n---\n".join(chunks)
#     if facts:
#         context += "\n\nRelated facts from knowledge graph:\n" + "\n".join(facts)

#     prompt = f"""Answer the question using only the context below.

#     Context:
#     {context}

#     Question: {question}"""

#     response = llm.invoke(prompt)
#     return response.content, context  # return context too, so you can feed it to RAGAS later

# # Quick test
# # answer, context_used = answer_question("what is the return policy if my item is bought last year")
# answer, context_used = answer_question("what is the return policy if my item is bought in a different country")

# print("=====context_used=====" + context_used)
# print(answer)

def answer_question(question: str):
    chunks, facts = hybrid_retrieve(question)

    context = "Relevant text excerpts:\n" + "\n---\n".join(chunks)
    if facts:
        context += "\n\nRelated facts from knowledge graph:\n" + "\n".join(facts)

#     prompt = f"""Answer the question using only the context below.

# Context:
# {context}

# Question: {question}"""


    prompt = f"""Answer the question using only the context below.

Give a direct, focused answer in 1-3 sentences that addresses exactly what was asked — nothing more. Do not include unrelated policy details, addresses, or general notes unless the question specifically asks for them.

Do not infer, generalize, or add interpretation beyond what the context explicitly states. If the context doesn't explicitly address part of the question, say so rather than guessing.

Context:
{context}

Question: {question}"""

    response = llm.invoke(prompt)

    # RAGAS wants contexts as a list — combine chunks + facts as separate list items
    ragas_contexts = chunks + facts

    return response.content, ragas_contexts


answer, ragas_contexts = answer_question("what is the return policy if my item is bought in a different country")

print("ANSWER:", answer)
print("CONTEXTS:", ragas_contexts)