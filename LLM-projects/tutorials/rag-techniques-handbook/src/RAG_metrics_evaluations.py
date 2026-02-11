from llama_index.core.evaluation import RetrieverEvaluator, FaithfulnessEvaluator
from llama_index.core import ServiceContext, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
import pandas as pd
from typing import List, Dict


class RAGEvaluator:
    def __init__(self, openai_api_key: str):
        """Initialize evaluator with necessary components."""
        self.llm = OpenAI(temperature=0, model="gpt-4", api_key=openai_api_key)
        self.service_context = ServiceContext.from_defaults(llm=self.llm)
        self.faithfulness_evaluator = FaithfulnessEvaluator(
            service_context=self.service_context
        )

    def evaluate_retriever(
            self,
            retriever,
            qa_dataset
    ) -> pd.DataFrame:
        """
        Evaluate retriever using RetrieverEvaluator.

        Args:
            retriever: Index retriever to evaluate
            qa_dataset: Dataset containing questions and contexts

        Returns:
            DataFrame with MRR and hit rate metrics
        """
        retriever_evaluator = RetrieverEvaluator.from_metric_names(
            ["mrr", "hit_rate"],
            retriever=retriever
        )

        eval_results = await retriever_evaluator.aevaluate_dataset(qa_dataset)

        metric_dicts = []
        for eval_result in eval_results:
            metric_dict = eval_result.metric_vals_dict
            metric_dicts.append(metric_dict)

        results_df = pd.DataFrame(metric_dicts)

        return {
            "hit_rate": results_df["hit_rate"].mean(),
            "mrr": results_df["mrr"].mean()
        }

    def evaluate_response_quality(
            self,
            query_engine,
            eval_questions: List[str],
            ground_truth: List[str]
    ) -> Dict:
        """
        Evaluate response quality using RAGAS metrics.

        Args:
            query_engine: Query engine to evaluate
            eval_questions: List of evaluation questions
            ground_truth: List of ground truth answers

        Returns:
            Dict containing scores for each metric
        """
        from ragas.integrations.llama_index import evaluate

        # Prepare evaluation data
        eval_data = {
            "question": eval_questions,
            "ground_truth": ground_truth
        }

        # Define metrics
        metrics = [
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall
        ]

        # Run evaluation
        results = evaluate(
            query_engine,
            eval_data,
            metrics=metrics
        )

        return results

    def evaluate_faithfulness(self, response) -> bool:
        """
        Evaluate faithfulness of a single response.

        Args:
            response: Response object from query engine

        Returns:
            Boolean indicating if response is faithful
        """
        eval_result = self.faithfulness_evaluator.evaluate_response(
            response=response
        )
        return eval_result.passing


# Example usage
if __name__ == "__main__":
    # Initialize evaluator
    evaluator = RAGEvaluator("your-openai-api-key")

    # Example evaluation questions
    eval_questions = [
        "What is the capital of France?",
        "Who wrote Romeo and Juliet?"
    ]

    ground_truth = [
        "Paris is the capital of France.",
        "William Shakespeare wrote Romeo and Juliet."
    ]

    # Create and evaluate query engine
    # Note: This is a simplified example - you'd need to set up your actual index and query engine
    from llama_index.core import Document, VectorStoreIndex

    documents = [Document(text="Paris is the capital of France.")]
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()

    # Evaluate retrieval
    retriever = index.as_retriever()
    retrieval_metrics = evaluator.evaluate_retriever(
        retriever,
        qa_dataset={"queries": eval_questions}  # Simplified dataset structure
    )

    # Evaluate response quality
    quality_metrics = evaluator.evaluate_response_quality(
        query_engine,
        eval_questions,
        ground_truth
    )

    print("Retrieval Metrics:", retrieval_metrics)
    print("Quality Metrics:", quality_metrics)