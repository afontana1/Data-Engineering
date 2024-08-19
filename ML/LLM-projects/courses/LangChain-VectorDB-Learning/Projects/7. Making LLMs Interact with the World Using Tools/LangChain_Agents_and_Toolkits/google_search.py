from langchain.llms import OpenAI
from langchain.agents import initialize_agent, load_tools, AgentType
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"] 
GOOGLE_CSE_ID = os.environ["GOOGLE_CSE_ID"]

# define the language model that we want the agent to use.
llm = OpenAI(model_name="text-davinci-003", temperature=0)

# load the google-search tool
tools = load_tools(["google-search"])

# initialize an agent
agent = initialize_agent(
    tools,
    llm,
    # gives the freedom to choose any of the defined tools to provide context for the model based on their description.
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  
)

print( agent("What is the national drink in Spain?") )