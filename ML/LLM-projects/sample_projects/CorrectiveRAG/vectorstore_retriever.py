from langchain_community.vectorstores import Chroma
from embeddings import CustomOllamaEmbeddings


class VectorStoreRetriever:
    """
    Creates a vector store from a list of documents and provides a retriever.

    Args:
        documents (list): A list of documents to be indexed.
        collection_name (str): The name of the Chroma collection.
        embedding_model (str): The name of the embedding model to use.
        embedding_url (str, optional): The URL of the embedding model service. Defaults to "http://localhost:11434".
    """

    def __init__(
        self,
        documents,
        collection_name,
        embedding_model,
        embedding_url="http://localhost:11434",
    ):

        self.documents = documents
        self.collection_name = collection_name
        self.embedding = CustomOllamaEmbeddings(
            model=embedding_model, base_url=embedding_url
        )
        self.vectorstore = Chroma.from_documents(
            documents=self.documents,
            collection_name=self.collection_name,
            embedding=self.embedding,
        )

    def get_retriever(self):
        """
        Returns a retriever for the vector store.

        Returns:
            langchain.vectorstores.base.VectorStoreRetriever: A retriever object.
        """
        return self.vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 2}
        )
