from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
hf = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)

documents = ["Document 1", "Document 2", "Document 3"]
doc_embeddings = hf.embed_documents(documents)