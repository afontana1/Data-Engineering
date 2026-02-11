import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
ACTIVELOOP_TOKEN = os.environ["ACTIVELOOP_TOKEN"]

# We scrape several Artificial Intelligence news

import requests
from newspaper import Article # https://github.com/codelucas/newspaper
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

article_urls = [
    "https://www.artificialintelligence-news.com/2023/05/23/meta-open-source-speech-ai-models-support-over-1100-languages/",
    "https://www.artificialintelligence-news.com/2023/05/18/beijing-launches-campaign-against-ai-generated-misinformation/"
    "https://www.artificialintelligence-news.com/2023/05/16/openai-ceo-ai-regulation-is-essential/",
    "https://www.artificialintelligence-news.com/2023/05/15/jay-migliaccio-ibm-watson-on-leveraging-ai-to-improve-productivity/",
    "https://www.artificialintelligence-news.com/2023/05/15/iurii-milovanov-softserve-how-ai-ml-is-helping-boost-innovation-and-personalisation/",
    "https://www.artificialintelligence-news.com/2023/05/11/ai-and-big-data-expo-north-america-begins-in-less-than-one-week/",
    "https://www.artificialintelligence-news.com/2023/05/11/eu-committees-green-light-ai-act/",
    "https://www.artificialintelligence-news.com/2023/05/09/wozniak-warns-ai-will-power-next-gen-scams/",
    "https://www.artificialintelligence-news.com/2023/05/09/infocepts-ceo-shashank-garg-on-the-da-market-shifts-and-impact-of-ai-on-data-analytics/",
    "https://www.artificialintelligence-news.com/2023/05/02/ai-godfather-warns-dangers-and-quits-google/",
    "https://www.artificialintelligence-news.com/2023/04/28/palantir-demos-how-ai-can-used-military/",
    "https://www.artificialintelligence-news.com/2023/04/26/ftc-chairwoman-no-ai-exemption-to-existing-laws/",
    "https://www.artificialintelligence-news.com/2023/04/24/bill-gates-ai-teaching-kids-literacy-within-18-months/",
    "https://www.artificialintelligence-news.com/2023/04/21/google-creates-new-ai-division-to-challenge-openai/"
]

session = requests.Session()
pages_content = [] # where we save the scraped articles

for url in article_urls:
    try:
        time.sleep(2) # sleep two seconds for gentle scraping
        response = session.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            article = Article(url)
            article.download() # download HTML of webpage
            article.parse() # parse HTML to extract the article text
            pages_content.append({ "url": url, "text": article.text })
        else:
            print(f"Failed to fetch article at {url}")
    except Exception as e:
        print(f"Error occurred while fetching article at {url}: {e}")

#If an error occurs while fetching an article, we catch the exception and print
#an error message. This ensures that even if one article fails to download,
#the rest of the articles can still be processed.

# We'll use an embedding model to compute our documents' embeddings
from langchain.embeddings.openai import OpenAIEmbeddings

# We'll store the documents and their embeddings in the deep lake vector db
from langchain.vectorstores import DeepLake

# Setup deep lake
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# create Deep Lake dataset
# TODO: use your organization id here. (by default, org id is your username)
my_activeloop_org_id = "<YOUR-ACTIVELOOP-ORG-ID>"
my_activeloop_dataset_name = "langchain_course_analysis_outline"
dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_dataset_name}"
db = DeepLake(dataset_path=dataset_path, embedding_function=embeddings)

# We split the article texts into small chunks

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

all_texts = []
for d in pages_content:
    chunks = text_splitter.split_text(d["text"])
    for chunk in chunks:
        all_texts.append(chunk)
        
# we add all the chunks to the Deep lake
db.add_texts(all_texts)

# Get the retriever object from the deep lake db object and set the number
# of retrieved documents to 3
retriever = db.as_retriever()
retriever.search_kwargs['k'] = 3

# We define some variables that will be used inside our custom tool
CUSTOM_TOOL_DOCS_SEPARATOR ="\n---------------\n" # how to join together the retrieved docs to form a single string

# This is the function that defines our custom tool that retrieves relevant
# docs from Deep Lake
def retrieve_n_docs_tool(query: str) -> str:
    """Searches for relevant documents that may contain the answer to the query."""
    docs = retriever.get_relevant_documents(query)
    texts = [doc.page_content for doc in docs]
    texts_merged = "---------------\n" + CUSTOM_TOOL_DOCS_SEPARATOR.join(texts) + "\n---------------"
    return texts_merged

from langchain.agents.tools import Tool

# We create the tool that uses the "retrieve_n_docs_tool" function
tools = [
    Tool(
        name="Search Private Docs",
        func=retrieve_n_docs_tool,
        description="useful for when you need to answer questions about current events about Artificial Intelligence"
    )
]

from langchain.chat_models import ChatOpenAI
from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

# let's create the Plan and Execute agent
model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
planner = load_chat_planner(model)
executor = load_agent_executor(model, tools, verbose=True)
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

# we test the agent
response = agent.run("Write an overview of Artificial Intelligence regulations by governments by country")

print(response)