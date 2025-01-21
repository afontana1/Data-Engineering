import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
ACTIVELOOP_TOKE = os.environ["ACTIVELOOP_TOKEN"]

# We'll use an embedding model to compute the embeddings of our documents
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake

# instantiate embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# create Deep Lake dataset
# We'll store the documents and their embeddings in the deep lake vector db
# TODO: use your organization id here. (by default, org id is your username)
my_activeloop_org_id = "djpapzin"
my_activeloop_dataset_name = "langchain_course_custom_tool"
dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_dataset_name}"
db = DeepLake(dataset_path=dataset_path, embedding_function=embeddings)

# add faqs to the dataset
faqs = [
    "What is PayPal?\nPayPal is a digital wallet that follows you wherever you go. Pay any way you want. Link your credit cards to your PayPal Digital wallet, and when you want to pay, simply log in with your username and password and pick which one you want to use.",
    "Why should I use PayPal?\nIt's Fast! We will help you pay in just a few clicks. Enter your email address and password, and you're pretty much done! It's Simple! There's no need to run around searching for your wallet. Better yet, you don't need to type in your financial details again and again when making a purchase online. We make it simple for you to pay with just your email address and password.",
    "Is it secure?\nPayPal is the safer way to pay because we keep your financial information private. It isn't shared with anyone else when you shop, so you don't have to worry about paying businesses and people you don't know. On top of that, we've got your back. If your eligible purchase doesn't arrive or doesn't match its description, we will refund you the full purchase price plus shipping costs with PayPal's Buyer Protection program.",
    "Where can I use PayPal?\nThere are millions of places you can use PayPal worldwide. In addition to online stores, there are many charities that use PayPal to raise money. Find a list of charities you can donate to here. Additionally, you can send funds internationally to anyone almost anywhere in the world with PayPal. All you need is their email address. Sending payments abroad has never been easier.",
    "Do I need a balance in my account to use it?\nYou do not need to have any balance in your account to use PayPal. Similar to a physical wallet, when you are making a purchase, you can choose to pay for your items with any of the credit cards that are attached to your account. There is no need to pre-fund your account."
]
db.add_texts(faqs)

# Get the retriever object from the deep lake db object
retriever = db.as_retriever()

from langchain.agents import tool

# We define some variables that will be used inside our custom tool
# We're creating a custom tool that looks for relevant documents in our deep lake db
CUSTOM_TOOL_N_DOCS = 3 # number of retrieved docs from deep lake to consider
CUSTOM_TOOL_DOCS_SEPARATOR ="\n\n" # how to join together the retrieved docs to form a single string

# We use the tool decorator to wrap a function that will become our custom tool
# Note that the tool has a single string as input and returns a single string as output
# The name of the function will be the name of our custom tool
# The docstring of the function will be the description of our custom tool
# The description is used by the agent to decide whether to use the tool for a specific query
@tool
def retrieve_n_docs_tool(query: str) -> str:
    """ Searches for relevant documents that may contain the answer to the query."""
    docs = retriever.get_relevant_documents(query)[:CUSTOM_TOOL_N_DOCS]
    texts = [doc.page_content for doc in docs]
    texts_merged = CUSTOM_TOOL_DOCS_SEPARATOR.join(texts)
    return texts_merged

# Load a LLM to create an agent using our custom tool
from langchain.llms import OpenAI
# Classes for initializing the agent that will use the custom tool
from langchain.agents import initialize_agent, AgentType

# Let's create an agent that uses our custom tool
# We set verbose=True to check if the agent is using the tool for generating the final answer
llm = OpenAI(model="text-davinci-003", temperature=0)
agent = initialize_agent([retrieve_n_docs_tool], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

response = agent.run("Are my info kept private when I shop with Paypal?")
print(response)