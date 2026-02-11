import os.path
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from .embedding_interface import EMBInterface
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
import logging


# Configure basic logging
logging.basicConfig(level=logging.INFO)




class Huggingface_embedders(EMBInterface):

  def __init__(self,**kwargs):

        self.model_name = kwargs.get("model_name")
        self.model_path = kwargs.get("model_path")
        self.model_kwargs = kwargs.get("model_kwargs")
        self.encode_kwargs = kwargs.get("encode_kwargs")


  async def load_model(self)->HuggingFaceEmbeddings|SentenceTransformer:

         if os.path.exists(self.model_path):


                # Load exist embedding model

                 logging.info("Loading embedding model...")

                 embedding_model = HuggingFaceEmbeddings(
                     model_name=self.model_name,
                     model_kwargs=self.model_kwargs,
                     encode_kwargs=self.encode_kwargs  )

                 return embedding_model


         else:

                # Download from huggingface

                 os.makedirs(self.model_path, exist_ok=True)  # make directory for embedding model

                 logging.info("Downloading embedding model..")

                 embedding_model = SentenceTransformer(self.model_name)  # get model from sources

                 embedding_model.save(str(self.model_path)) # save the model 

                 
                 logging.info(f"Embedding Model downloaded Successfully at {self.model_path}...")

                 embedding_model = HuggingFaceEmbeddings(
                     model_name=self.model_name,
                     model_kwargs=self.model_kwargs,
                     encode_kwargs=self.encode_kwargs ) 

                 return embedding_model




