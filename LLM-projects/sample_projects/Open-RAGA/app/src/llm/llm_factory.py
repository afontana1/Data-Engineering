from .nvidia_chat_llm import Nvidia_chat_llm

class CHATLLMFactory:

   @staticmethod
   def create_chat_model_pipeline(llm_type,**kwargs):

       if llm_type== "nvidia":

        return Nvidia_chat_llm(**kwargs)