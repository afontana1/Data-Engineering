# The ConversationChain uses the ConversationBufferMemory class by default to provide a history of messages. This memory can save the previous conversations in form of variables. The class accepts the return_messages argument which is helpful for dealing with chat models. This is how the CoversationChain keep context under the hood.

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain import OpenAI, ConversationChain
from langchain import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate


memory = ConversationBufferMemory(return_messages=True)
memory.save_context({"input": "hi there!"}, {"output": "Hi there! It's nice to meet you. How can I help you today?"})

print( memory.load_memory_variables({}) )

llm = OpenAI(model_name="text-davinci-003", temperature=0)

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=ConversationBufferMemory()
)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

print( conversation.predict(input="Tell me a joke about elephants") )
print( conversation.predict(input="Who is the author of the Harry Potter series?") )
print( conversation.predict(input="What was the joke you told me earlier?") )

from langchain import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI."),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm, verbose=True)

user_message = "Tell me about the history of the Internet."
response = conversation(user_message)
print(response)

# User sends another message
user_message = "Who are some important figures in its development?"
response = conversation(user_message)
print(response)  # Chatbot responds with names of important figures, recalling the previous topic

user_message = "What did Tim Berners-Lee contribute?"
response = conversation(user_message)
print(response)