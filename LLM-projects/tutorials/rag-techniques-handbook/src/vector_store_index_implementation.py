from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import logging
from llama_index import VectorStoreIndex, Document
from llama_index.vector_stores import DeepLakeVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.evaluation import RetrieverEvaluator
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class VectorStoreConfig:
    """Configuration for Vector Store setup"""
    dataset_path: str
    chunk_size: int = 512
    chunk_overlap: int = 20
    use_deep_memory: bool = False
    enable_reranking: bool = False
    similarity_top_k: int = 10
    tensor_db: bool = True


class VectorStoreManager:
    """Manages Vector Store operations and configurations"""

    def __init__(self, config: VectorStoreConfig):
        """Initialize Vector Store Manager with configuration"""
        self.config = config
        self.vector_store = None
        self.index = None
        self.storage_context = None

    def initialize_vector_store(self) -> None:
        """Initialize and configure the vector store"""
        try:
            self.vector_store = DeepLakeVectorStore(
                dataset_path=self.config.dataset_path,
                overwrite=False,
                read_only=True,
                runtime={"tensor_db": self.config.tensor_db}
            )

            self.storage_context = StorageContext.from_defaults(
                vector_store=self.vector_store
            )

            logger.info("Vector store initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            raise

    def create_index(self, documents: List[Document]) -> None:
        """Create index from documents"""
        try:
            if not self.storage_context:
                raise ValueError("Storage context not initialized")

            self.index = VectorStoreIndex.from_documents(
                documents,
                storage_context=self.storage_context
            )

            logger.info("Index created successfully")

        except Exception as e:
            logger.error(f"Failed to create index: {str(e)}")
            raise

    def setup_query_engine(self, reranker: Optional[CohereRerank] = None):
        """Configure and return query engine"""
        if not self.index:
            raise ValueError("Index not initialized")

        query_engine_kwargs = {
            "similarity_top_k": self.config.similarity_top_k
        }

        if self.config.use_deep_memory:
            query_engine_kwargs["vector_store_kwargs"] = {"deep_memory": True}

        if self.config.enable_reranking and reranker:
            query_engine_kwargs["node_postprocessors"] = [reranker]

        return self.index.as_query_engine(**query_engine_kwargs)

    async def evaluate_performance(self, dataset) -> Dict[str, float]:
        """Evaluate retriever performance"""
        try:
            evaluator = RetrieverEvaluator.from_metric_names(
                ["mrr", "hit_rate"],
                retriever=self.index.as_retriever()
            )

            results = await evaluator.aevaluate_dataset(dataset)

            metrics = {
                "mrr": sum(r.metric_vals_dict["mrr"] for r in results) / len(results),
                "hit_rate": sum(r.metric_vals_dict["hit_rate"] for r in results) / len(results)
            }

            logger.info(f"Evaluation metrics: {metrics}")
            return metrics

        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            raise


def example_usage():
    """Example usage of VectorStoreManager"""
    # Configuration
    config = VectorStoreConfig(
        dataset_path="hub://organization/dataset",
        chunk_size=512,
        chunk_overlap=20,
        use_deep_memory=True,
        enable_reranking=True
    )

    # Initialize manager
    manager = VectorStoreManager(config)

    try:
        # Setup vector store
        manager.initialize_vector_store()

        # Create sample documents
        documents = [
            Document(text="Sample document 1"),
            Document(text="Sample document 2")
        ]

        # Create index
        manager.create_index(documents)

        # Setup query engine
        reranker = CohereRerank(api_key="your-api-key", top_n=5)
        query_engine = manager.setup_query_engine(reranker)

        # Example query
        response = query_engine.query("Sample query")
        print(f"Query response: {response}")

        # Evaluate performance
        async def run_evaluation():
            metrics = await manager.evaluate_performance(dataset)
            print(f"Performance metrics: {metrics}")

        asyncio.run(run_evaluation())

    except Exception as e:
        logger.error(f"Error in example usage: {str(e)}")
        raise


if __name__ == "__main__":
    example_usage()