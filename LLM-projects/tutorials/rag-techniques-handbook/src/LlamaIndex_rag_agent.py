from typing import List, Any, Dict
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.deeplake import DeepLakeVectorStore
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.agent.openai import OpenAIAgent
import os


class RAGAgent:
    """
    Implements a RAG system with integrated agent capabilities for
    multi-source querying and tool usage.
    """

    def __init__(self, openai_key: str, activeloop_token: str = None):
        """
        Initialize RAG Agent with necessary credentials.

        Args:
            openai_key: OpenAI API key
            activeloop_token: Optional Deep Lake token for vector store
        """
        os.environ['OPENAI_API_KEY'] = openai_key
        if activeloop_token:
            os.environ['ACTIVELOOP_TOKEN'] = activeloop_token
        self.query_tools = []
        self.function_tools = []

    def add_document_source(self,
                            file_path: str,
                            name: str,
                            description: str,
                            use_deeplake: bool = False,
                            deeplake_path: str = None) -> None:
        """
        Add a document source to the RAG system.

        Args:
            file_path: Path to document file
            name: Unique name for this data source
            description: Description of the data source's content
            use_deeplake: Whether to use Deep Lake vector store
            deeplake_path: Path for Deep Lake dataset
        """
        docs = SimpleDirectoryReader(input_files=[file_path]).load_data()

        if use_deeplake:
            vector_store = DeepLakeVectorStore(dataset_path=deeplake_path)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
        else:
            index = VectorStoreIndex.from_documents(docs)

        engine = index.as_query_engine(similarity_top_k=3)

        tool = QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name=name,
                description=description
            )
        )
        self.query_tools.append(tool)

    def add_function_tool(self, func: callable, name: str) -> None:
        """
        Add a custom function tool to the agent.

        Args:
            func: Function to add as tool
            name: Name for the function tool
        """
        tool = FunctionTool.from_defaults(fn=func, name=name)
        self.function_tools.append(tool)

    def create_agent(self, verbose: bool = True) -> OpenAIAgent:
        """
        Create an agent with all configured tools.

        Args:
            verbose: Whether to show detailed agent operations

        Returns:
            Configured OpenAI agent
        """
        all_tools = self.query_tools + self.function_tools
        return OpenAIAgent.from_tools(all_tools, verbose=verbose)


# Example usage
def example_usage():
    # Initialize agent
    agent = RAGAgent(
        openai_key="your-openai-key",
        activeloop_token="your-activeloop-token"  # Optional
    )

    # Add document sources
    agent.add_document_source(
        file_path="data/technical.txt",
        name="tech_docs",
        description="Technical documentation and specifications"
    )

    agent.add_document_source(
        file_path="data/general.txt",
        name="general_info",
        description="General information and FAQs",
        use_deeplake=True,
        deeplake_path="hub://org/dataset"
    )

    # Add custom function tool
    def calculate_total(items: List[Dict[str, float]]) -> float:
        """Calculate total price from list of items"""
        return sum(item['price'] for item in items)

    agent.add_function_tool(calculate_total, "calculate_total")

    # Create and use agent
    openai_agent = agent.create_agent()
    response = openai_agent.chat("What's the total price of items X, Y, and Z?")
    print(response)


if __name__ == "__main__":
    example_usage()