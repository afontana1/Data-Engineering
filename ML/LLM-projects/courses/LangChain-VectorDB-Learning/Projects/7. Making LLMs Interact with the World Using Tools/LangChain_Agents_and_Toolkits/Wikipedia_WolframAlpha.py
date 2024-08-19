import os
from langchain. utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, load_tools, AgentType

WOLFRAM_ALPHA_APPID = os.environ["WOLFRAM_ALPHA_APPID"]

wolfram = WolframAlphaAPIWrapper()

llm = OpenAI(model_name="text-davinci-003", temperature=0)

tools = load_tools(["wolfram-alpha", "wikipedia"], llm=llm)

agent = initialize_agent(
		tools,
		llm,
		agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
		verbose=True
	)

agent.run("Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?")