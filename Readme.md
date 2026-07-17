My first RAG project!

this project documents a question and answering system.
it starts from a simple "what is the refund policy" question

query-memory.py is my first attempt at building a RAG pipeline
1. used llamaindex to store policy data in memory
2. cohere for creation and returning of embeddings
3. my questions were hardcoded strings for Claude to handle query and return answer to user

i then decided to move to graphRAG
1. switched orchestration from LlamaIndex to Langchain, data store to Neo4j
2. updated query logic. script will use vector similarity search to find top chunks, then invoke graph traversal on those chunks. graph traversal goes beyond top k chunks to find connected entities and relationships
3. Query is still used for Claude in order to get to answer

Questions
1. Simple, already have answer to: what is the return policy if my item is bought last year
2. Vague, no direct answer:  what is the return policy if my item is bought in a different country
==========
Todos
1. how to handle multiple input documents
2. i dont know what document types can be handled
