import logging
import os

import agent
import document_loader
import vectorstore_retriever
import workflow
import yaml_reader

YAML_FILE_PATH = "application.yaml"
logger = logging.getLogger(__name__)


class App:
    """
    This class represents the main application for information retrieval.

    It handles configuration loading, data ingestion, and workflow building
    for processing user queries.
    """

    def __init__(
        self,
        doc_loader=document_loader.DocumentLoaderSplitter,
        embedding_model=None,
    ):
        self.vector_store_retriever = None
        self.app = None
        yaml_config_reader = yaml_reader.YamlConfigReader(YAML_FILE_PATH)
        self.collection_name = yaml_config_reader.get("collection_name")
        self.embedding_model = (
            embedding_model
            if embedding_model
            else yaml_config_reader.get("embedding_model")
        )
        self.model_name = yaml_config_reader.get("model")
        self.ollama_url = yaml_config_reader.get("ollama_url")
        os.environ["GOOGLE_CSE_ID"] = yaml_config_reader.get("GOOGLE_CSE_ID")
        os.environ["GOOGLE_API_KEY"] = yaml_config_reader.get("GOOGLE_API_KEY")
        self.agent_helper = agent.AgentHelper(self.model_name, self.ollama_url)
        self.loader = doc_loader

    def ingest(self, pdf_file_paths=[], urls=[]):
        """
        Ingests documents from provided URLs or PDF files into the vector store.

        This method creates a DocumentLoaderSplitter instance to load and split documents.
        It then creates a VectorStoreRetriever instance to store the documents in the vector store
        and build a retriever for querying the documents. Finally, it builds the workflow using
        the AgentHelper and the retrieved components.

        Args:
            pdf_file_paths (list[str], optional): A list of paths to PDF files to ingest.
            Defaults to [].
            urls (list[str], optional): A list of URLs to ingest documents from. Defaults to [].
        """
        doc_loader_splitter = self.loader(urls, pdf_file_paths)
        doc_splits = doc_loader_splitter.load_and_split_documents()
        self.vector_store_retriever = vectorstore_retriever.VectorStoreRetriever(
            documents=doc_splits,
            collection_name=self.collection_name,
            embedding_model=self.embedding_model,
            embedding_url=self.ollama_url,
        )
        retriever = self.vector_store_retriever.get_retriever()

        (
            retrieval_grader,
            summary_chain,
            rag_chain,
            hallucination_grader,
            answer_grader,
            web_search_tool,
        ) = self.agent_helper.get_agents()
        wf = workflow.Workflow(
            retriever,
            doc_splits,
            summary_chain,
            rag_chain,
            retrieval_grader,
            hallucination_grader,
            answer_grader,
            web_search_tool,
        )
        self.app = wf.build()

    def invoke(self, query, retries=2):
        """
        Invokes the workflow to process a user query.

        This method checks if the workflow is built. If not, it returns a message indicating
        that no documents are loaded. Otherwise, it runs the workflow with the provided query
        and allows for retries in case of failures.

        Args:
            query (str): The user query to be processed.
            retries (int): number of retries after which for websearch is done.
        """
        if not self.app:
            return "Please add a PDF document or enter an URL."
        return self.app.stream({"question": query, "retries": retries})

    def clear(self):
        """
        Clear out the vector_store and the app instance
        """
        self.vector_store_retriever = None
        self.app = None
