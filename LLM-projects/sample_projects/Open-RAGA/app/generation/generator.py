from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.generation.prompt_templates import get_template  # your custom function







class ResponseGenerator:
  
    def __init__(self, llm, template_name: str = "prompt_main"):
        self.llm = llm
        self.prompt_template: PromptTemplate = get_template(template_name['prompt_main'])
    
    def generate(self, context: str, query: str)-> dict:
        prompt = self.prompt_template
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run({"query": query})
        return (result,chain)
        
