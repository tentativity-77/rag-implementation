#this scripe does an ingestion

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_anthropic import ChatAnthropic
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph

load_dotenv()

# 1. Load your PDF (same as your existing pipeline)
loader = PyPDFLoader("data/nintendo.pdf")  # <- swap in your actual PDF path
documents = loader.load()


# 2. Chunk it — graph extraction works better on slightly larger chunks
#    than pure vector RAG, since entities/relationships need surrounding context
splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
chunks = splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks")

# 3. Set up Claude as the extraction engine
llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)

# 4. LLMGraphTransformer reads each chunk and pulls out (Entity)-[RELATIONSHIP]->(Entity) triples
graph_transformer = LLMGraphTransformer(llm=llm)

print("Extracting graph from chunks (this calls Claude once per chunk, may take a few minutes)...")
graph_documents = graph_transformer.convert_to_graph_documents(chunks)

# 5. Connect to your local Neo4j instance and push the graph in
graph = Neo4jGraph(
    url=os.environ["NEO4J_URI"],
    username=os.environ["NEO4J_USERNAME"],
    password=os.environ["NEO4J_PASSWORD"],
)

graph.add_graph_documents(
    graph_documents,
    baseEntityLabel=True,
    include_source=True,  # links each entity back to the source chunk — useful for hybrid retrieval later
)

print("Done. Check Neo4j Browser — run `MATCH (n) RETURN n LIMIT 50` to see your graph.")