#this script ingests PDF, stores it in memory, asks cohere to embed it before running a question

#--- SETUP
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

#--- BUILD THE INDEX
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

#--- QUERY
# the model responses will differ based on the questions being asked 
# response = query_engine.query("What is the return policy?")
# response = query_engine.query("What is the return policy if  not in its original condition?")
# response = query_engine.query("What is the return policy if it is of a different colour than expected?")

question = ("What is the return period for Nintendo products?")
# question = ("What is the return policy if it is purchased from a different country from where the customer is residing?")

response = query_engine.query(question)
print(response)
print("--------")
print("RETRIEVED CHUNKS:")
for node in response.source_nodes:
    print(node.text)
    print(f"SCORE: {node.score}")
    print("--------")

# ---- RAGAS EVALUATION ----
# ---- RAGAS EVALUATION ----
from ragas import evaluate
from ragas.llms import llm_factory
from langchain_anthropic import ChatAnthropic
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision
from ragas import EvaluationDataset, SingleTurnSample
from langchain_cohere import CohereEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper


from anthropic import Anthropic as AnthropicClient

# Set up Claude as the RAGAS judge
ragas_client = AnthropicClient(api_key=os.getenv("ANTHROPIC_API_KEY"))

ragas_llm = LangchainLLMWrapper(
    ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0.0
    )
)

# Structure your data
answer = str(response)
contexts = [node.text for node in response.source_nodes]
reference = "Nintendo's return policy does not have a specific provision for cross-border purchases. Items must be purchased directly from the Nintendo Store, and there are separate return addresses for U.S. and Canadian residents only."

ragas_embeddings = LangchainEmbeddingsWrapper(
    CohereEmbeddings(
        model="embed-english-v3.0",
        cohere_api_key=os.getenv("COHERE_API_KEY")
    )
)

sample = SingleTurnSample(
    user_input=question,
    response=answer,
    retrieved_contexts=contexts,
    reference=reference
)

dataset = EvaluationDataset(samples=[sample])

# Run evaluation
results = evaluate(
    dataset,
    metrics=[Faithfulness(), AnswerRelevancy(), ContextPrecision()],
    llm=ragas_llm,
    embeddings=ragas_embeddings
)

print(results)