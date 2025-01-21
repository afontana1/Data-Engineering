from langchain.embeddings import OpenAIEmbeddings
import faiss
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore

# Define the embedding model
embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002")

# Initialize the vectorstore
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

from langchain import OpenAI
from langchain.experimental import BabyAGI

# set the goal
goal = "Plan a trip to the Grand Canyon"

# create thebabyagi agent
# If max_iterations is None, the agent may go on forever if stuck in loops
baby_agi = BabyAGI.from_llm(
    llm=OpenAI(model="text-davinci-003", temperature=0),
    vectorstore=vectorstore,
    verbose=False,
    max_iterations=3
)
response = baby_agi({"objective": goal})