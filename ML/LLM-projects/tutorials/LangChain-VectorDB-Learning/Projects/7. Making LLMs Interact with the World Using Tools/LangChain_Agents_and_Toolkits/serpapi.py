from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

llm = OpenAI(model_name="text-davinci-003", temperature=0)
tools = load_tools(['serpapi', 'requests_all'], llm=llm, serpapi_api_key=SERPAPI_API_KEY)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.run("What is the capital of spain")