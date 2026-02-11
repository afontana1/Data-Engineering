import os

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from app.scripts.prepare_data import get_file_contents
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)


# Class to load Faiss(Facebook AI similarity search)

class Faiss_db:
   
  def __init__(self,**kwargs):
        self.vector_store_path = kwargs.get("vector_store_path")
        self.embedding_model =  kwargs.get("embedding_model")
        self.chunk_size  =  int(kwargs.get("chunk_size"))
        self.chunk_overlap  =  int(kwargs.get("chunk_overlap"))
        self.allow_dangerous_deserialization = kwargs.get("allow_dangerous_deserialization",True)
        self.index_name = kwargs.get("index_name","index")
        self.docs_path = str(kwargs.get("docs_path"))

  async  def load_faiss_db(self):
        if(os.path.exists(self.vector_store_path)):
            vector_db =   FAISS.load_local(folder_path = self.vector_store_path,index_name=self.index_name ,embeddings=self.embedding_model, allow_dangerous_deserialization=self.allow_dangerous_deserialization)
            return vector_db
            logging.info("database loaded successfully..")

        else:
              self.create_vector_embeddings(docs_path=self.docs_path,output_index_path=self.vector_store_path)
              vector_db = FAISS.load_local(folder_path=self.vector_store_path, index_name=self.index_name,
                                           embeddings=self.embedding_model,
                                           allow_dangerous_deserialization=self.allow_dangerous_deserialization)
              return vector_db

   # Create vector Embeddings datastore
  def create_vector_embeddings(self,docs_path,output_index_path):


        # Split into chunks
        text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size
                                              , chunk_overlap=self.chunk_overlap)

        docs = text_splitter.create_documents(get_file_contents(docs_path))

        try:

            vectorstore = FAISS.from_documents(docs, self.embedding_model)

            vectorstore.save_local(output_index_path)

            print(f"Vector created successfully in {output_index_path}:- ")



        except Exception as e:


            logging.error("error in creating vectors...",e)




  def append_embeddings(self,index_name,vector_db_path,docs_path,output_index_path,allow_dangerous_deserialization):


            # Split into chunks
            text_splitter = CharacterTextSplitter(chunk_size=self.chunk_size
                                                  , chunk_overlap=self.chunk_overlap)
            docs = text_splitter.create_documents(get_file_contents(docs_path))


            vectorstore =  FAISS.load_local(folder_path=vector_db_path,index_name=index_name ,embeddings=self.embedding_model, allow_dangerous_deserialization=self.allow_dangerous_deserialization)

            # 3. Add new texts
            vectorstore.add_texts(docs)

            # 4. Save updated index
            vectorstore.save_local(output_index_path)


            logging.info(f"New docs added successfully in {self.vector_store_path}:- ")

