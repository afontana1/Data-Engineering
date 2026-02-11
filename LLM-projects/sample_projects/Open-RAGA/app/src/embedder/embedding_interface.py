from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

class EMBInterface:

    async def load_model(self)->HuggingFaceEmbeddings|SentenceTransformer:


        pass
