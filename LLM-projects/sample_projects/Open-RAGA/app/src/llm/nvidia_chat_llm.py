from langchain_nvidia_ai_endpoints import ChatNVIDIA
import logging
# Configure basic logging
logging.basicConfig(level=logging.INFO)




class Nvidia_chat_llm():


    def __init__(self,**kwargs):

        self.model_name = kwargs.get("model_name")
        self.temperature = kwargs.get("temperature")
        self.max_tokens = kwargs.get("max_tokens")
        self.api_key = kwargs.get("api_key")



    async def load_model(self)->ChatNVIDIA:


        llm = ChatNVIDIA(
            model=self.model_name,
            api_key=self.api_key,
            temperature=self.temperature,
            max_tokens= self.max_tokens)

        logging.info(f"{self.model_name} loaded successfully..")

        return llm




