"""
Advanced RAG Techniques Implementation Template
This module demonstrates various RAG (Retrieval Augmented Generation) techniques using LlamaIndex
including query construction, expansion, transformation, and advanced retrieval methods.

Author: Manel Soler
License: MIT
"""

import os
from typing import List, Dict, Any, Optional
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.vector_stores.deeplake import DeepLakeVectorStore
from llama_index.postprocessor.cohere_rerank import CohereRerank
import cohere


class AdvancedRAGEngine:
    """
    A comprehensive RAG implementation combining multiple advanced techniques.
    Includes query construction, expansion, transformation, and advanced retrieval methods.
    """

    def __init__(
            self,
            documents_path: str,
            openai_api_key: str,
            activeloop_token: str,
            cohere_api_key: str,
            chunk_size: int = 512,
            chunk_overlap: int = 64
    ):
        """
        Initialize the RAG engine with necessary credentials and configurations.

        Args:
            documents_path: Path to the directory containing documents
            openai_api_key: OpenAI API key for embeddings and LLM
            activeloop_token: ActiveLoop token for vector store
            cohere_api_key: Cohere API key for reranking
            chunk_size: Size of text chunks for processing
            chunk_overlap: Overlap between chunks
        """
        # Set environment variables
        os.environ['OPENAI_API_KEY'] = openai_api_key
        os.environ['ACTIVELOOP_TOKEN'] = activeloop_token
        self.cohere_client = cohere.Client(cohere_api_key)

        # Configure basic settings
        Settings.chunk_size = chunk_size
        Settings.chunk_overlap = chunk_overlap
        self.node_parser = Settings.node_parser

        # Load and process documents
        self.documents = SimpleDirectoryReader(documents_path).load_data()
        self.nodes = self.node_parser.get_nodes_from_documents(self.documents)

        # Initialize vector store
        self.setup_vector_store()

    def setup_vector_store(
            self,
            org_id: str = "your_org_id",
            dataset_name: str = "advanced_rag_dataset"
    ):
        """
        Set up the vector store using DeepLake.

        Args:
            org_id: ActiveLoop organization ID
            dataset_name: Name for the dataset
        """
        dataset_path = f"hub://{org_id}/{dataset_name}"
        self.vector_store = DeepLakeVectorStore(
            dataset_path=dataset_path,
            overwrite=False
        )

        # Setup storage context and index
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        self.storage_context.docstore.add_documents(self.nodes)
        self.vector_index = VectorStoreIndex(
            self.nodes,
            storage_context=self.storage_context
        )

    def basic_query_engine(
            self,
            similarity_top_k: int = 10,
            streaming: bool = True
    ):
        """
        Create a basic query engine with configurable parameters.

        Args:
            similarity_top_k: Number of similar documents to retrieve
            streaming: Whether to enable response streaming

        Returns:
            Query engine instance
        """
        return self.vector_index.as_query_engine(
            streaming=streaming,
            similarity_top_k=similarity_top_k
        )

    def reranking_query_engine(
            self,
            similarity_top_k: int = 10,
            rerank_top_n: int = 2
    ):
        """
        Create a query engine with Cohere reranking.

        Args:
            similarity_top_k: Number of initial documents to retrieve
            rerank_top_n: Number of documents to keep after reranking

        Returns:
            Query engine with reranking
        """
        cohere_rerank = CohereRerank(
            api_key=os.environ.get('COHERE_API_KEY'),
            top_n=rerank_top_n
        )

        return self.vector_index.as_query_engine(
            similarity_top_k=similarity_top_k,
            node_postprocessors=[cohere_rerank]
        )

    def sub_question_query_engine(
            self,
            similarity_top_k: int = 10,
            tool_name: str = "advanced_rag",
            tool_description: str = "Advanced RAG query engine for complex queries"
    ):
        """
        Create a sub-question query engine for complex queries.

        Args:
            similarity_top_k: Number of similar documents to retrieve
            tool_name: Name for the query engine tool
            tool_description: Description of the tool's functionality

        Returns:
            SubQuestionQueryEngine instance
        """
        base_query_engine = self.vector_index.as_query_engine(
            similarity_top_k=similarity_top_k
        )

        query_engine_tools = [
            QueryEngineTool(
                query_engine=base_query_engine,
                metadata=ToolMetadata(
                    name=tool_name,
                    description=tool_description
                )
            )
        ]

        return SubQuestionQueryEngine.from_defaults(
            query_engine_tools=query_engine_tools,
            use_async=True
        )

    def process_query(
            self,
            query: str,
            engine_type: str = "basic",
            **kwargs
    ):
        """
        Process a query using the specified engine type.

        Args:
            query: The query string
            engine_type: Type of query engine to use ('basic', 'rerank', 'sub_question')
            **kwargs: Additional arguments for the specific engine type

        Returns:
            Query response
        """
        engines = {
            "basic": self.basic_query_engine,
            "rerank": self.reranking_query_engine,
            "sub_question": self.sub_question_query_engine
        }

        if engine_type not in engines:
            raise ValueError(f"Unsupported engine type: {engine_type}")

        query_engine = engines[engine_type](**kwargs)
        return query_engine.query(query)


def main():
    """Example usage of the AdvancedRAGEngine"""

    # Initialize the engine
    rag_engine = AdvancedRAGEngine(
        documents_path="./documents",
        openai_api_key="your_openai_key",
        activeloop_token="your_activeloop_token",
        cohere_api_key="your_cohere_key"
    )

    # Example queries using different techniques
    query = "What is the main concept of the document?"

    # Basic query
    print("\nBasic Query Result:")
    response = rag_engine.process_query(query, engine_type="basic")
    print(response)

    # Query with reranking
    print("\nReranked Query Result:")
    response = rag_engine.process_query(
        query,
        engine_type="rerank",
        similarity_top_k=10,
        rerank_top_n=2
    )
    print(response)

    # Complex query using sub-questions
    complex_query = "Compare and contrast the main themes in different sections of the document"
    print("\nSub-Question Query Result:")
    response = rag_engine.process_query(
        complex_query,
        engine_type="sub_question"
    )
    print(response)


if __name__ == "__main__":
    main()