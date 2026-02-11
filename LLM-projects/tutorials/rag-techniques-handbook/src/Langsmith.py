"""
LangSmith Implementation Example

This module demonstrates how to set up and use LangSmith for LLM application
development, evaluation, and monitoring.
"""

import os
from typing import Dict, List, Optional
from datetime import datetime

from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import DeepLake
from langchain.evaluation import load_evaluator
from langchain_core.runnables import RunnablePassthrough


class LangSmithManager:
    """
    Manages LangSmith integration for LLM application development and monitoring.
    """

    def __init__(
            self,
            api_key: str,
            project_name: str,
            endpoint: str = "https://api.smith.langchain.com"
    ):
        """
        Initialize LangSmith manager with necessary credentials and configuration.

        Args:
            api_key (str): LangSmith API key
            project_name (str): Name of the project for tracking
            endpoint (str): LangSmith API endpoint
        """
        self.setup_environment(api_key, project_name, endpoint)
        self.llm = ChatOpenAI(temperature=0)
        self.output_parser = StrOutputParser()

    @staticmethod
    def setup_environment(api_key: str, project_name: str, endpoint: str) -> None:
        """Set up environment variables for LangSmith."""
        os.environ["LANGCHAIN_API_KEY"] = api_key
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = endpoint
        os.environ["LANGCHAIN_PROJECT"] = project_name

    def create_prompt_template(
            self,
            template: str,
            handle: str,
            public: bool = False
    ) -> ChatPromptTemplate:
        """
        Create and version a prompt template.

        Args:
            template (str): Prompt template string
            handle (str): Unique identifier for the prompt
            public (bool): Whether to make the prompt public

        Returns:
            ChatPromptTemplate: Created prompt template
        """
        prompt = ChatPromptTemplate.from_template(template)
        hub.push(handle, prompt, new_repo_is_public=public)
        return prompt

    def create_qa_chain(
            self,
            vectorstore: DeepLake,
            prompt_handle: str
    ) -> RetrievalQA:
        """
        Create a question-answering chain with tracing enabled.

        Args:
            vectorstore (DeepLake): Initialized vector store
            prompt_handle (str): Handle of the prompt to use

        Returns:
            RetrievalQA: Configured QA chain
        """
        prompt = hub.pull(prompt_handle)

        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=vectorstore.as_retriever(),
            chain_type_kwargs={"prompt": prompt}
        )

        return qa_chain

    def evaluate_responses(
            self,
            predictions: List[str],
            references: List[str],
            criteria: str = "accuracy"
    ) -> List[Dict]:
        """
        Evaluate model responses against references.

        Args:
            predictions (List[str]): Model generated responses
            references (List[str]): Ground truth references
            criteria (str): Evaluation criteria

        Returns:
            List[Dict]: Evaluation results
        """
        evaluator = load_evaluator("criteria", criteria=criteria)
        results = []

        for pred, ref in zip(predictions, references):
            result = evaluator.evaluate_strings(
                prediction=pred,
                reference=ref
            )
            results.append(result)

        return results

    def create_monitored_chain(
            self,
            prompt_template: ChatPromptTemplate
    ) -> RunnablePassthrough:
        """
        Create a chain with monitoring enabled.

        Args:
            prompt_template (ChatPromptTemplate): Prompt template to use

        Returns:
            RunnablePassthrough: Monitored chain
        """
        chain = (
                prompt_template
                | self.llm
                | self.output_parser
        )

        return chain


def main():
    """Example usage of LangSmithManager."""

    # Initialize manager
    manager = LangSmithManager(
        api_key="your-api-key",
        project_name="example-project"
    )

    # Create and version a prompt
    prompt = manager.create_prompt_template(
        template="Write a summary of {topic} in {word_count} words.",
        handle="summary-generator"
    )

    # Create monitored chain
    chain = manager.create_monitored_chain(prompt)

    # Run chain with tracing
    response = chain.invoke({
        "topic": "artificial intelligence",
        "word_count": "100"
    })

    # Evaluate responses
    predictions = [response]
    references = ["AI is a branch of computer science..."]  # Reference answer

    results = manager.evaluate_responses(predictions, references)

    print("Evaluation Results:", results)


if __name__ == "__main__":
    # Example error handling
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {str(e)}")