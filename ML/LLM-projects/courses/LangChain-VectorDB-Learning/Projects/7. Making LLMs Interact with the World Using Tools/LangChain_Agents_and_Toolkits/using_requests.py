from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents import initialize_agent, load_tools, AgentType

llm = OpenAI(model_name="text-davinci-003", temperature=0)

tools = load_tools(["requests_all"], llm=llm)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
  )

response = agent.run("Get the list of users at https://644696c1ee791e1e2903b0bb.mockapi.io/user and tell me the total number of users")