import os
from langchain. utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, load_tools, AgentType

WOLFRAM_ALPHA_APPID = os.environ["WOLFRAM_ALPHA_APPID"]

wolfram = WolframAlphaAPIWrapper()
result = wolfram.run("What is 2x+5 = -3x + 7?")
print(result)  # Output: 'x = 2/5'

tools = load_tools(["wolfram-alpha"])

llm = OpenAI(model_name="text-davinci-003", temperature=0)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  
)

print( agent.run("How many days until the next Solar eclipse") )