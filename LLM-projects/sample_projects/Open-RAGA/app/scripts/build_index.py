from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import prepare_data
import yaml
import os

root_path = os.path.dirname(os.path.abspath(__file__))

# Load a .yaml or .yml file
with open(root_path+"/config/dev/model_config.yaml", "r") as file:
    model_config = yaml.safe_load(file)



model_name = model_config['embedding_model']['name']    
model_keywords = model_config['embedding_model']['model_kwargs']
encode_kwargs = model_config['embedding_model']['encode_kwargs']


# Load a .yaml or .yml file
with open(root_path+"/config/dev/app_config.yaml", "r") as file:
    app_config = yaml.safe_load(file)



chunk_size = app_config['retriever']['cunk_size']
chunk_overlap = app_config['retriever']['chunk_overlap']
vectorstore_path = app_config['vector_store']['persist_path']




# get embeddings model

def get_embedding_model():

  embedding_model = HuggingFaceEmbeddings(
        model_name= model_name,
        model_kwargs=model_keywords,
        encode_kwargs=encode_kwargs   
    )

  return  embedding_model


docs_path  = root_path+"/data"+"/preprocessed"


def get_embeddings(docs_path= docs_path,vectorstore_path=vectorstore_path):

    # Split into chunks
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size
                                          , chunk_overlap=chunk_overlap)
    docs = text_splitter.create_documents(prepare_data.get_file_contents(docs_path))


    vectorstore  = FAISS.from_documents(docs, get_embedding_model())
     
    vectorstore.save_local(vectorstore_path)
    print(f"Vector Created successfully in {vectorstore_path}:- ") 
