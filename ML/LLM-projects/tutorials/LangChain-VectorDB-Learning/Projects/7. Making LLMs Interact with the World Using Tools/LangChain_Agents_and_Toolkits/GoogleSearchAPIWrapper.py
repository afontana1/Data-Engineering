from langchain. utilities import GoogleSearchAPIWrapper
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"] 
GOOGLE_CSE_ID = os.environ["GOOGLE_CSE_ID"]

# As a standalone utility
# GoogleSearchAPIWrapper to receive k top search results given a query. 
search = GoogleSearchAPIWrapper()
search.results("What is the capital of Spain?", 3)