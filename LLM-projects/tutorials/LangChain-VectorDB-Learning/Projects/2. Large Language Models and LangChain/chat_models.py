from langchain.chat_models import ChatOpenAI
from langchain.schema import (
  HumanMessage,
  SystemMessage
)

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

messages = [
	SystemMessage(content="You are a helpful assistant that translates English to French."),
	HumanMessage(content="Translate the following sentence: I love programming.")
]

chat(messages)