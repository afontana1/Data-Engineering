from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, load_tools, AgentType

llm = OpenAI(model_name="text-davinci-003", temperature=0)

tools = load_tools(["wikipedia"])

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  
)



print( agent.run("What is Nostradamus know for") )