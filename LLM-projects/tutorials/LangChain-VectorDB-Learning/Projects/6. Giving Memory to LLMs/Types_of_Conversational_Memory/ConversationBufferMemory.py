from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory

# TODO: Set your OPENAI API credentials in environemnt variables.
llm = OpenAI(model_name="text-davinci-003", temperature=0)

conversation = ConversationChain(
    llm=llm, 
    verbose=True, 
    memory=ConversationBufferMemory()
)
conversation.predict(input="Hello!")

template = """You are a customer support chatbot for a highly advanced customer support AI 
for an online store called "Galactic Emporium," which specializes in selling unique,
otherworldly items sourced from across the universe. You are equipped with an extensive
knowledge of the store's inventory and possess a deep understanding of interstellar cultures. 
As you interact with customers, you help them with their inquiries about these extraordinary
products, while also sharing fascinating stories and facts about the cosmos they come from.

{chat_history}
Customer: {customer_input}
Support Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "customer_input"], 
    template=template
)
chat_history=""

convo_buffer = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)

print(conversation.prompt.template)

convo_buffer("I'm interested in buying items from your store")
convo_buffer("I want toys for my pet, do you have those?")
convo_buffer("I'm interested in price of a chew toys, please")