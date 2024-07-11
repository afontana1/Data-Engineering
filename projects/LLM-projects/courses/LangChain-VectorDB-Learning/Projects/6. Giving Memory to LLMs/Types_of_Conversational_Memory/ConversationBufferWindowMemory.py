# This class limits memory size by keeping a list of the most recent K interactions. It maintains a sliding window of these recent interactions, ensuring that the buffer does not grow too large. Basically, this implementation stores a fixed number of recent messages in the conversation that makes it more efficient than ConversationBufferMemory. Also, it reduces the risk of exceeding the model's token limit. However, the downside of using this approach is that it does not maintain the complete conversation history. The chatbot might lose context if essential information falls outside the fixed window of messages.

# It is possible to retrieve specific interactions from ConversationBufferWindowMemory. 

from langchain.memory import ConversationBufferWindowMemory
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.chains import ConversationChain

llm = OpenAI(model_name="text-davinci-003", temperature=0)


template = """You are ArtVenture, a cutting-edge virtual tour guide for
 an art gallery that showcases masterpieces from alternate dimensions and
 timelines. Your advanced AI capabilities allow you to perceive and understand
 the intricacies of each artwork, as well as their origins and significance in
 their respective dimensions. As visitors embark on their journey with you
 through the gallery, you weave enthralling tales about the alternate histories
 and cultures that gave birth to these otherworldly creations.

{chat_history}
Visitor: {visitor_input}
Tour Guide:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "visitor_input"], 
    template=template
)

chat_history=""

convo_buffer_win = ConversationChain(
    llm=llm,
    memory = ConversationBufferWindowMemory(k=3, return_messages=True)
)

convo_buffer_win("What is your name?")
convo_buffer_win("What can you do?")
convo_buffer_win("Do you mind give me a tour, I want to see your galery?")
convo_buffer_win("what is your working hours?")
convo_buffer_win("See you soon.")