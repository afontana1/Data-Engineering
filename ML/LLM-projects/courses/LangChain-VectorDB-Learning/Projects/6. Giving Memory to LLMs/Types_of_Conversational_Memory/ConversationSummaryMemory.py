# ConversationSummaryBufferMemory is a memory management strategy that combines the ideas of keeping a buffer of recent interactions in memory and compiling old interactions into a summary. It extracts key information from previous interactions and condenses it into a shorter, more manageable format.  Here is a list of pros and cons of ConversationSummaryMemory.

from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory
from langchain import OpenAI
from langchain.prompts import PromptTemplate


llm = OpenAI(model_name="text-davinci-003", temperature=0)

# Create a ConversationChain with ConversationSummaryMemory
conversation_with_summary = ConversationChain(
    llm=llm, 
    memory=ConversationSummaryMemory(llm=llm),
    verbose=True
)

# Example conversation
response = conversation_with_summary.predict(input="Hi, what's up?")
print(response)

prompt = PromptTemplate(
    input_variables=["topic"],
    template="The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.\nCurrent conversation:\n{topic}",
)

from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory

llm = OpenAI(temperature=0)
conversation_with_summary = ConversationChain(
    llm=llm,
    memory=ConversationSummaryBufferMemory(llm=OpenAI(), max_token_limit=40),
    verbose=True
)
conversation_with_summary.predict(input="Hi, what's up?")
conversation_with_summary.predict(input="Just working on writing some documentation!")
response = conversation_with_summary.predict(input="For LangChain! Have you heard of it?")
print(response)