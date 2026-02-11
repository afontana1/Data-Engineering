from .faiss_db import Faiss_db

class VECTORDBFactory:

   @staticmethod
   def create_vector_db_pipeline(db_type,**kwargs):

       if db_type== "faiss":

         return  Faiss_db(**kwargs)