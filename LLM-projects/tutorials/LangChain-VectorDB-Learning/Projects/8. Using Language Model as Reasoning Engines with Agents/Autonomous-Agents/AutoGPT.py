import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
GOOGLE_CSE_ID = os.environ["GOOGLE_CSE_ID"]

from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import Tool
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool

#Set up the tools
search = GoogleSearchAPIWrapper()
tools = [
    Tool(
        name = "search",
        func=search.run,
        description="Useful for when you need to answer questions about current events. You should ask targeted questions",
        return_direct=True
    ),
    WriteFileTool(),
    ReadFileTool(),
]

# Set up the memory
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings

embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002")
embedding_size = 1536

import faiss
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

# Set up the model and AutoGPT
from langchain.experimental import AutoGPT
from langchain.chat_models import ChatOpenAI

agent = AutoGPT.from_llm_and_tools(
    ai_name="Jim",
    ai_role="Assistant",
    tools=tools,
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    memory=vectorstore.as_retriever()
)

# Set verbose to be true
agent.chain.verbose = True

task = "Provide an analysis of the major historical events that led to the slavery of Africans"

agent.run([task])