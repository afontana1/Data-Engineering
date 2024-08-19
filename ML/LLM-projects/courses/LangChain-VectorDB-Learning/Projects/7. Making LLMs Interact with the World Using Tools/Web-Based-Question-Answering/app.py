import os

GOOGLE_CSE_ID = os.environ["GOOGLE_CSE_ID"]
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

from langchain.llms import OpenAI
from langchain.agents import Tool, initialize_agent, AgentType

from langchain.utilities import GoogleSearchAPIWrapper, PythonREPL

search = GoogleSearchAPIWrapper()
python_repl = PythonREPL()

llm = OpenAI(model="text-davinci-003", temperature=0)

toolkit = [
    Tool(
        name="google-search",
        func=search.run,
        description="useful for when you need to search Google to answer questions about current events"
    ),
    Tool(
        name="python_repl",
        description="A Python shell. Use this to execute Python commands. Input should be a valid Python command. Useful for saving strings to files.",
        func=python_repl.run
    )
]

agent = initialize_agent(
	toolkit,
	llm,
	agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
	verbose=True
)

agent.run("Find the birth date of Napoleon Bonaparte and save it to a file 'answer.txt'.")

with open('answer.txt', 'w') as f:
    f.write('Napoleon Bonaparte was born on August 15, 1769')
    
query = "Find when Napoleon Bonaparte died and append this information " \
    "to the content of the 'answer.txt' file in a new line."

agent.run(query)