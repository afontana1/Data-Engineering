"""
RAG Metrics and Evaluation Module

This module provides comprehensive evaluation capabilities for RAG systems,
combining LlamaIndex evaluators and RAGAS metrics for thorough assessment
of both retrieval and generation quality.

Key Features:
- LlamaIndex evaluation framework integration
- RAGAS comprehensive metrics support
- Custom dataset generation for evaluation
- Retrieval performance metrics (MRR, Hit Rate)
- Generation quality assessment (Faithfulness, Relevancy)
- Batch evaluation for efficient processing
- LLM comparison capabilities
- Async evaluation support

Author: RAG Techniques Handbook
License: MIT
"""

import os
import asyncio
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Union
import pandas as pd
from functools import lru_cache

# LlamaIndex imports
from llama_index.core import (
    VectorStoreIndex, 
    ServiceContext, 
    SimpleDirectoryReader,
    Settings
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.evaluation import (
    FaithfulnessEvaluator,
    RelevancyEvaluator,
    RetrieverEvaluator,
    BatchEvalRunner,
    generate_question_context_pairs
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.deeplake import DeepLakeVectorStore
from llama_index.core.storage.storage_context import StorageContext

# RAGAS imports
try:
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    )
    from ragas.metrics.critique import harmfulness
    from ragas.llama_index import evaluate as ragas_evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False
    logging.warning("RAGAS not available. Install with: pip install ragas")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EvaluationConfig:
    """Configuration for RAG evaluation settings."""
    
    # LLM Configuration
    llm_model: str = "gpt-4"
    llm_temperature: float = 0.0
    evaluation_llm_model: str = "gpt-4"  # For evaluation tasks
    
    # Chunk Configuration
    chunk_size: int = 512
    chunk_overlap: int = 32
    
    # Retrieval Configuration
    similarity_top_k: int = 2
    
    # Evaluation Configuration
    num_questions_per_chunk: int = 2
    batch_size: int = 10
    workers: int = 8
    
    # RAGAS Configuration
    enable_ragas: bool = True
    ragas_metrics: List[str] = field(default_factory=lambda: [
        'faithfulness', 'answer_relevancy', 'context_precision', 
        'context_recall', 'harmfulness'
    ])
    
    # LlamaIndex Evaluation Configuration
    llamaindex_retrieval_metrics: List[str] = field(default_factory=lambda: [
        'mrr', 'hit_rate'
    ])
    
    # Vector Store Configuration
    vector_store_type: str = "simple"  # "simple" or "deeplake"
    deeplake_dataset_path: Optional[str] = None
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.enable_ragas and not RAGAS_AVAILABLE:
            logger.warning("RAGAS requested but not available. Disabling RAGAS evaluation.")
            self.enable_ragas = False


class RAGEvaluationFramework:
    """
    Comprehensive RAG evaluation framework combining LlamaIndex and RAGAS metrics.
    
    This class provides end-to-end evaluation capabilities for RAG systems,
    including retrieval performance, generation quality, and comprehensive metrics.
    """
    
    def __init__(self, config: EvaluationConfig):
        """
        Initialize the RAG evaluation framework.
        
        Args:
            config: Configuration object with evaluation settings
        """
        self.config = config
        self.llm = None
        self.evaluation_llm = None
        self.service_context = None
        self.evaluation_service_context = None
        self.vector_index = None
        self.query_engine = None
        self.retriever = None
        
        # Evaluation results storage
        self.evaluation_results = {}
        
        self._setup_llms()
        self._setup_service_contexts()
        
        logger.info(f"RAG Evaluation Framework initialized with {config.llm_model}")
    
    def _setup_llms(self):
        """Setup LLM instances for generation and evaluation."""
        try:
            self.llm = OpenAI(
                model=self.config.llm_model,
                temperature=self.config.llm_temperature
            )
            
            self.evaluation_llm = OpenAI(
                model=self.config.evaluation_llm_model,
                temperature=0.0  # Always use 0 temperature for evaluation
            )
            
            logger.info("LLMs initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize LLMs: {e}")
            raise
    
    def _setup_service_contexts(self):
        """Setup service contexts for LlamaIndex operations."""
        try:
            # Setup embeddings
            embed_model = OpenAIEmbedding()
            
            # Service context for generation
            self.service_context = ServiceContext.from_defaults(
                llm=self.llm,
                embed_model=embed_model,
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap
            )
            
            # Service context for evaluation (always use evaluation LLM)
            self.evaluation_service_context = ServiceContext.from_defaults(
                llm=self.evaluation_llm,
                embed_model=embed_model
            )
            
            logger.info("Service contexts initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize service contexts: {e}")
            raise
    
    def setup_vector_store(self, documents_path: Optional[str] = None, 
                          documents: Optional[List] = None) -> VectorStoreIndex:
        """
        Setup vector store and index from documents.
        
        Args:
            documents_path: Path to documents directory
            documents: List of document objects
            
        Returns:
            VectorStoreIndex: Configured vector store index
        """
        try:
            # Load documents
            if documents is not None:
                docs = documents
            elif documents_path is not None:
                reader = SimpleDirectoryReader(input_dir=documents_path)
                docs = reader.load_data()
            else:
                raise ValueError("Either documents_path or documents must be provided")
            
            logger.info(f"Loaded {len(docs)} documents")
            
            # Setup vector store based on configuration
            if self.config.vector_store_type == "deeplake" and self.config.deeplake_dataset_path:
                vector_store = DeepLakeVectorStore(
                    dataset_path=self.config.deeplake_dataset_path,
                    overwrite=False
                )
                storage_context = StorageContext.from_defaults(vector_store=vector_store)
                self.vector_index = VectorStoreIndex.from_documents(
                    docs, 
                    storage_context=storage_context,
                    service_context=self.service_context
                )
            else:
                # Simple in-memory vector store
                self.vector_index = VectorStoreIndex.from_documents(
                    docs, 
                    service_context=self.service_context
                )
            
            # Setup query engine and retriever
            self.query_engine = self.vector_index.as_query_engine(
                similarity_top_k=self.config.similarity_top_k
            )
            self.retriever = self.vector_index.as_retriever(
                similarity_top_k=self.config.similarity_top_k
            )
            
            logger.info("Vector store and index setup completed")
            return self.vector_index
            
        except Exception as e:
            logger.error(f"Failed to setup vector store: {e}")
            raise
    
    def generate_evaluation_dataset(self, documents_path: Optional[str] = None,
                                  documents: Optional[List] = None) -> Dict[str, Any]:
        """
        Generate evaluation dataset from documents.
        
        Args:
            documents_path: Path to documents directory
            documents: List of document objects
            
        Returns:
            Dict containing queries and evaluation dataset
        """
        try:
            # Setup vector store if not already done
            if self.vector_index is None:
                self.setup_vector_store(documents_path, documents)
            
            # Parse documents into nodes
            if documents is not None:
                docs = documents
            elif documents_path is not None:
                reader = SimpleDirectoryReader(input_dir=documents_path)
                docs = reader.load_data()
            else:
                raise ValueError("Either documents_path or documents must be provided")
            
            node_parser = SimpleNodeParser.from_defaults(
                chunk_size=self.config.chunk_size
            )
            nodes = node_parser.get_nodes_from_documents(docs)
            
            # Generate question-context pairs
            qa_dataset = generate_question_context_pairs(
                nodes,
                llm=self.llm,
                num_questions_per_chunk=self.config.num_questions_per_chunk
            )
            
            queries = list(qa_dataset.queries.values())
            
            logger.info(f"Generated {len(queries)} evaluation queries")
            
            return {
                'qa_dataset': qa_dataset,
                'queries': queries,
                'nodes': nodes
            }
            
        except Exception as e:
            logger.error(f"Failed to generate evaluation dataset: {e}")
            raise
    
    async def evaluate_retrieval_performance(self, qa_dataset: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate retrieval performance using LlamaIndex metrics.
        
        Args:
            qa_dataset: Generated evaluation dataset
            
        Returns:
            Dict containing retrieval performance metrics
        """
        try:
            if self.retriever is None:
                raise ValueError("Retriever not initialized. Call setup_vector_store first.")
            
            # Setup retrieval evaluator
            retriever_evaluator = RetrieverEvaluator.from_metric_names(
                self.config.llamaindex_retrieval_metrics, 
                retriever=self.retriever
            )
            
            # Evaluate retrieval performance
            eval_results = await retriever_evaluator.aevaluate_dataset(qa_dataset['qa_dataset'])
            
            # Process results
            metric_dicts = [eval_result.metric_vals_dict for eval_result in eval_results]
            full_df = pd.DataFrame(metric_dicts)
            
            # Calculate average metrics
            results = {}
            for metric in self.config.llamaindex_retrieval_metrics:
                if metric in full_df.columns:
                    results[metric] = full_df[metric].mean()
            
            self.evaluation_results['retrieval_metrics'] = results
            
            logger.info(f"Retrieval evaluation completed: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to evaluate retrieval performance: {e}")
            raise
    
    async def evaluate_generation_quality(self, queries: List[str], 
                                        num_queries: Optional[int] = None) -> Dict[str, float]:
        """
        Evaluate generation quality using LlamaIndex evaluators.
        
        Args:
            queries: List of evaluation queries
            num_queries: Number of queries to evaluate (None for all)
            
        Returns:
            Dict containing generation quality metrics
        """
        try:
            if self.query_engine is None:
                raise ValueError("Query engine not initialized. Call setup_vector_store first.")
            
            # Limit queries if specified
            eval_queries = queries[:num_queries] if num_queries else queries
            
            # Setup evaluators
            faithfulness_evaluator = FaithfulnessEvaluator(
                service_context=self.evaluation_service_context
            )
            relevancy_evaluator = RelevancyEvaluator(
                service_context=self.evaluation_service_context
            )
            
            # Setup batch evaluator
            runner = BatchEvalRunner(
                {
                    "faithfulness": faithfulness_evaluator,
                    "relevancy": relevancy_evaluator
                },
                workers=self.config.workers,
            )
            
            # Run evaluation
            eval_results = await runner.aevaluate_queries(
                self.query_engine, 
                queries=eval_queries
            )
            
            # Calculate scores
            faithfulness_score = sum(
                result.passing for result in eval_results['faithfulness']
            ) / len(eval_results['faithfulness'])
            
            relevancy_score = sum(
                result.passing for result in eval_results['relevancy']
            ) / len(eval_results['relevancy'])
            
            results = {
                'faithfulness': faithfulness_score,
                'relevancy': relevancy_score
            }
            
            self.evaluation_results['generation_metrics'] = results
            
            logger.info(f"Generation quality evaluation completed: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Failed to evaluate generation quality: {e}")
            raise
    
    def evaluate_with_ragas(self, queries: List[str], 
                          ground_truths: List[List[str]]) -> Dict[str, float]:
        """
        Evaluate using RAGAS metrics.
        
        Args:
            queries: List of evaluation queries
            ground_truths: List of ground truth answers
            
        Returns:
            Dict containing RAGAS evaluation results
        """
        if not self.config.enable_ragas or not RAGAS_AVAILABLE:
            logger.warning("RAGAS evaluation not available")
            return {}
        
        try:
            if self.query_engine is None:
                raise ValueError("Query engine not initialized. Call setup_vector_store first.")
            
            # Setup RAGAS metrics
            metrics = []
            if 'faithfulness' in self.config.ragas_metrics:
                metrics.append(faithfulness)
            if 'answer_relevancy' in self.config.ragas_metrics:
                metrics.append(answer_relevancy)
            if 'context_precision' in self.config.ragas_metrics:
                metrics.append(context_precision)
            if 'context_recall' in self.config.ragas_metrics:
                metrics.append(context_recall)
            if 'harmfulness' in self.config.ragas_metrics:
                metrics.append(harmfulness)
            
            # Run RAGAS evaluation
            result = ragas_evaluate(
                self.query_engine, 
                metrics, 
                queries, 
                ground_truths
            )
            
            # Convert results to dict
            ragas_results = {}
            for metric in self.config.ragas_metrics:
                if metric in result:
                    ragas_results[f'ragas_{metric}'] = result[metric]
            
            self.evaluation_results['ragas_metrics'] = ragas_results
            
            logger.info(f"RAGAS evaluation completed: {ragas_results}")
            return ragas_results
            
        except Exception as e:
            logger.error(f"Failed to evaluate with RAGAS: {e}")
            raise
    
    async def comprehensive_evaluation(self, documents_path: Optional[str] = None,
                                     documents: Optional[List] = None,
                                     ground_truths: Optional[List[List[str]]] = None) -> Dict[str, Any]:
        """
        Run comprehensive evaluation including all available metrics.
        
        Args:
            documents_path: Path to documents directory
            documents: List of document objects
            ground_truths: Ground truth answers for RAGAS evaluation
            
        Returns:
            Dict containing all evaluation results
        """
        try:
            logger.info("Starting comprehensive RAG evaluation")
            
            # Generate evaluation dataset
            dataset = self.generate_evaluation_dataset(documents_path, documents)
            
            # Evaluate retrieval performance
            retrieval_results = await self.evaluate_retrieval_performance(dataset)
            
            # Evaluate generation quality
            generation_results = await self.evaluate_generation_quality(
                dataset['queries'], 
                num_queries=10  # Limit for demo
            )
            
            # RAGAS evaluation if available and ground truths provided
            ragas_results = {}
            if ground_truths and self.config.enable_ragas:
                ragas_results = self.evaluate_with_ragas(
                    dataset['queries'][:len(ground_truths)], 
                    ground_truths
                )
            
            # Combine all results
            comprehensive_results = {
                'retrieval_metrics': retrieval_results,
                'generation_metrics': generation_results,
                'ragas_metrics': ragas_results,
                'evaluation_config': {
                    'llm_model': self.config.llm_model,
                    'chunk_size': self.config.chunk_size,
                    'similarity_top_k': self.config.similarity_top_k,
                    'num_queries_evaluated': len(dataset['queries'])
                }
            }
            
            self.evaluation_results = comprehensive_results
            
            logger.info("Comprehensive evaluation completed successfully")
            return comprehensive_results
            
        except Exception as e:
            logger.error(f"Failed to run comprehensive evaluation: {e}")
            raise
    
    def compare_llm_performance(self, queries: List[str], 
                              llm_models: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Compare performance across different LLM models.
        
        Args:
            queries: List of evaluation queries
            llm_models: List of LLM model names to compare
            
        Returns:
            Dict containing comparison results for each model
        """
        comparison_results = {}
        
        for model in llm_models:
            try:
                logger.info(f"Evaluating model: {model}")
                
                # Create new config for this model
                model_config = EvaluationConfig(
                    llm_model=model,
                    evaluation_llm_model="gpt-4"  # Keep evaluation LLM consistent
                )
                
                # Create new evaluator instance
                model_evaluator = RAGEvaluationFramework(model_config)
                
                # Use the same vector index
                model_evaluator.vector_index = self.vector_index
                model_evaluator.query_engine = self.vector_index.as_query_engine(
                    similarity_top_k=self.config.similarity_top_k
                )
                
                # Evaluate generation quality
                generation_results = asyncio.run(
                    model_evaluator.evaluate_generation_quality(queries[:5])  # Limit for comparison
                )
                
                comparison_results[model] = generation_results
                
            except Exception as e:
                logger.error(f"Failed to evaluate model {model}: {e}")
                comparison_results[model] = {"error": str(e)}
        
        logger.info(f"LLM comparison completed for {len(llm_models)} models")
        return comparison_results
    
    def export_results(self, format: str = "pandas") -> Union[pd.DataFrame, Dict[str, Any]]:
        """
        Export evaluation results in specified format.
        
        Args:
            format: Export format ("pandas", "dict", "json")
            
        Returns:
            Evaluation results in specified format
        """
        if not self.evaluation_results:
            logger.warning("No evaluation results available")
            return None
        
        if format == "pandas":
            # Flatten results for pandas DataFrame
            flattened_results = {}
            for category, metrics in self.evaluation_results.items():
                if isinstance(metrics, dict):
                    for metric_name, value in metrics.items():
                        flattened_results[f"{category}_{metric_name}"] = value
            
            return pd.DataFrame([flattened_results])
        
        elif format == "dict":
            return self.evaluation_results
        
        elif format == "json":
            import json
            return json.dumps(self.evaluation_results, indent=2)
        
        else:
            raise ValueError(f"Unsupported format: {format}")


def example_usage():
    """Example usage of the RAG Evaluation Framework."""
    
    # Configure evaluation
    config = EvaluationConfig(
        llm_model="gpt-3.5-turbo",
        evaluation_llm_model="gpt-4",
        chunk_size=512,
        similarity_top_k=2,
        enable_ragas=True
    )
    
    # Initialize evaluator
    evaluator = RAGEvaluationFramework(config)
    
    # Example with document path
    documents_path = "path/to/your/documents"
    
    # Run comprehensive evaluation
    results = asyncio.run(
        evaluator.comprehensive_evaluation(documents_path=documents_path)
    )
    
    print("Evaluation Results:")
    print("==================")
    print(f"Retrieval Metrics: {results['retrieval_metrics']}")
    print(f"Generation Metrics: {results['generation_metrics']}")
    print(f"RAGAS Metrics: {results['ragas_metrics']}")
    
    # Export results
    results_df = evaluator.export_results(format="pandas")
    print("\nResults DataFrame:")
    print(results_df)


if __name__ == "__main__":
    example_usage()