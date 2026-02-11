from .huggingface_embedder import Huggingface_embedders

class EMBFactory:

   @staticmethod
   def create_embedder_model_pipeline(emb_type,**kwargs):

       if emb_type== "huggingface":

          return Huggingface_embedders(**kwargs)