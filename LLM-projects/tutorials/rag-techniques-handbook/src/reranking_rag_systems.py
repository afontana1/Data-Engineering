from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
import logging
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.postprocessor import SentenceTransformerRerank
from llama_index.core.postprocessor import LLMRerank
from llama_index.evaluation import RetrieverEvaluator
import asyncio
import time
from functools import lru_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RerankerConfig:
    """Configuration for reranker setup"""
    reranker_type: str  # 'cohere', 'sentence_transformer', or 'llm'
    top_k: int = 5
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    threshold: float = 0.0
    use_cache: bool = True


class RerankerManager:
    """Manages different types of rerankers and their operations"""

    def __init__(self, config: RerankerConfig):
        """Initialize RerankerManager with configuration"""
        self.config = config
        self.reranker = self._initialize_reranker()
        self._cache = {}

    def _initialize_reranker(self):
        """Initialize appropriate reranker based on configuration"""
        try:
            if self.config.reranker_type == "cohere":
                if not self.config.api_key:
                    raise ValueError("API key required for Cohere reranker")
                return CohereRerank(
                    api_key=self.config.api_key,
                    top_n=self.config.top_k,
                    model=self.config.model_name or "rerank-english-v2.0"
                )
            elif self.config.reranker_type == "sentence_transformer":
                return SentenceTransformerRerank(
                    model_name=self.config.model_name or "cross-encoder/ms-marco-MiniLM-L-6-v2",
                    top_n=self.config.top_k
                )
            elif self.config.reranker_type == "llm":
                return LLMRerank(
                    choice_batch_size=self.config.top_k,
                    top_n=self.config.top_k
                )
            else:
                raise ValueError(f"Unsupported reranker type: {self.config.reranker_type}")

        except Exception as e:
            logger.error(f"Failed to initialize reranker: {str(e)}")
            raise

    @lru_cache(maxsize=1000)
    def _cached_rerank(self, query: str, documents: tuple) -> List[Dict]:
        """Cached version of reranking operation"""
        return self.reranker.rerank(query, list(documents))

    def rerank_results(self, query: str, documents: List[Any]) -> List[Dict]:
        """Rerank documents based on query"""
        try:
            start_time = time.time()

            if self.config.use_cache:
                # Convert documents to tuple for caching
                doc_tuple = tuple(str(doc) for doc in documents)
                results = self._cached_rerank(query, doc_tuple)
            else:
                results = self.reranker.rerank(query, documents)

            # Filter results based on threshold
            filtered_results = [
                r for r in results
                if r.get('relevance_score', 0) >= self.config.threshold
            ]

            logger.info(
                f"Reranking completed in {time.time() - start_time:.2f}s. "
                f"Found {len(filtered_results)} results above threshold."
            )

            return filtered_results

        except Exception as e:
            logger.error(f"Reranking failed: {str(e)}")
            raise

    async def evaluate_reranker(self, eval_dataset) -> Dict[str, float]:
        """Evaluate reranker performance"""
        try:
            evaluator = RetrieverEvaluator.from_metric_names(
                ["mrr", "hit_rate"],
                retriever=None  # Will be set in evaluation
            )

            results = await evaluator.aevaluate_dataset(
                eval_dataset,
                workers=4
            )

            metrics = {
                "mrr": sum(r.metric_vals_dict["mrr"] for r in results) / len(results),
                "hit_rate": sum(r.metric_vals_dict["hit_rate"] for r in results) / len(results)
            }

            logger.info(f"Reranker evaluation metrics: {metrics}")
            return metrics

        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            raise


class EnsembleReranker:
    """Combines multiple rerankers for better results"""

    def __init__(self, rerankers: List[RerankerManager], weights: List[float]):
        """Initialize ensemble with multiple rerankers and their weights"""
        if len(rerankers) != len(weights):
            raise ValueError("Number of rerankers must match number of weights")
        self.rerankers = rerankers
        self.weights = weights

    def rerank(self, query: str, documents: List[Any]) -> List[Dict]:
        """Combine results from multiple rerankers"""
        try:
            final_scores = {}

            for reranker, weight in zip(self.rerankers, self.weights):
                results = reranker.rerank_results(query, documents)

                for result in results:
                    doc_id = result.get('id', str(result))
                    score = result.get('relevance_score', 0)
                    final_scores[doc_id] = final_scores.get(doc_id, 0) + weight * score

            # Sort by final weighted scores
            sorted_results = sorted(
                final_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )

            return sorted_results

        except Exception as e:
            logger.error(f"Ensemble reranking failed: {str(e)}")
            raise


def example_usage():
    """Example usage of reranking functionality"""
    # Configure individual rerankers
    cohere_config = RerankerConfig(
        reranker_type="cohere",
        top_k=5,
        api_key="your-api-key"
    )

    st_config = RerankerConfig(
        reranker_type="sentence_transformer",
        top_k=5
    )

    # Initialize reranker managers
    cohere_reranker = RerankerManager(cohere_config)
    st_reranker = RerankerManager(st_config)

    # Example documents
    documents = [
        {"id": 1, "text": "Sample document 1"},
        {"id": 2, "text": "Sample document 2"}
    ]

    # Single reranker usage
    results = cohere_reranker.rerank_results(
        "sample query",
        documents
    )
    print(f"Single reranker results: {results}")

    # Ensemble reranker usage
    ensemble = EnsembleReranker(
        rerankers=[cohere_reranker, st_reranker],
        weights=[0.7, 0.3]
    )

    ensemble_results = ensemble.rerank(
        "sample query",
        documents
    )
    print(f"Ensemble results: {ensemble_results}")


if __name__ == "__main__":
    example_usage()