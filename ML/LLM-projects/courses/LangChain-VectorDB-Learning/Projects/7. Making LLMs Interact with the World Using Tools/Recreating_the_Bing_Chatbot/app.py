from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)

template = """You are an assistant that answers the following question correctly and honestly: {question}\n\n"""
prompt_template = PromptTemplate(input_variables=["question"], template=template)

question_chain = LLMChain(llm=llm, prompt=prompt_template)

question_chain.run("what is the latest fast and furious movie?")