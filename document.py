#load env vars
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file into environment variables

from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.readers.file import PyMuPDFReader
from llama_index.core.node_parser import SentenceSplitter


# Configure LlamaIndex to use Claude + Cohere embeddings
Settings.llm = Anthropic(
        model="claude-sonnet-4-6",
        temperature=0.0,
        api_key=os.getenv("ANTHROPIC_API_KEY")
 
)
Settings.embed_model = CohereEmbedding(
    model_name="embed-english-v3.0",
    api_key=os.getenv("COHERE_API_KEY")
)

# print(Settings.llm)        # should show Anthropic/Claude
# print(Settings.embed_model) # should show CohereEmbedding

# before reading and understanding the document, chunking
Settings.text_splitter = SentenceSplitter(
    chunk_size=512,
    chunk_overlap=50
)

# Everything else stays exactly the same
# all these are from Llamaindex 
documents = SimpleDirectoryReader("data",
    file_extractor={".pdf": PyMuPDFReader()}
).load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine() #query_engine is by claude 

# the model responses will differ based on the questions being asked 
# response = query_engine.query("What is the return policy?")
# response = query_engine.query("What is the return policy if  not in its original condition?")
# response = query_engine.query("What is the return policy if it is of a different colour than expected?")
response = query_engine.query("What is the return policy if it is purchased from a different country from where the customer is residing?")
print(response)
print("--------")
print("RETRIEVED CHUNKS:")
for node in response.source_nodes:
    print(node.text)
    print(f"SCORE: {node.score}")
    print("--------")