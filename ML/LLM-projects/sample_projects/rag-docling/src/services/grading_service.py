from typing import List, Dict, Any, Literal
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from models.model_manager import get_model
import logging

logger = logging.getLogger(__name__)

class Grade(BaseModel):
    """Binary score for relevance check."""
    binary_score: Literal["yes", "no"] = Field(description="Relevance score 'yes' or 'no'")
    explanation: str = Field(description="Explanation for the score")

class GradingService:
    """Service for grading document relevance and checking hallucinations."""
    
    def __init__(self):
        self.model = get_model()
    
    def grade_documents(self, question: str, documents: List[Dict[str, Any]]) -> Grade:
        """
        Grade the relevance of retrieved documents to a question.
        
        Args:
            question: The user's question
            documents: List of retrieved documents
            
        Returns:
            Grade object with binary score and explanation
        """
        try:
            # Prepare context from documents
            context = "\n\n".join(
                f"Document {i+1}:\n{doc.get('content', '')}"
                for i, doc in enumerate(documents)
            )
            
            # Create grading prompt
            prompt = f"""You are a grader assessing relevance of retrieved documents to a user question.

Question: {question}

Retrieved Documents:
{context}

Task: Evaluate if these documents are relevant to answering the question.
Consider:
1. Semantic relevance to the question
2. Presence of key information needed
3. Quality and completeness of information

Provide:
1. A binary score ("yes" or "no")
2. A brief explanation of your decision

Format your response as:
binary_score: [yes/no]
explanation: [your explanation]"""

            # Get structured output from model
            llm_with_structured_output = self.model.with_structured_output(Grade)
            result = llm_with_structured_output.invoke(prompt)
            
            logger.info(f"Document grading result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in document grading: {str(e)}")
            return Grade(
                binary_score="no",
                explanation=f"Error during grading: {str(e)}"
            )
    
    def check_hallucination(self, question: str, documents: List[Dict[str, Any]], 
                          generation: str) -> Grade:
        """
        Check if the generated response is grounded in the documents.
        
        Args:
            question: Original question
            documents: Source documents
            generation: Generated response
            
        Returns:
            Grade indicating if response is grounded in facts
        """
        try:
            # Prepare context
            context = "\n\n".join(
                f"Document {i+1}:\n{doc.get('content', '')}"
                for i, doc in enumerate(documents)
            )
            
            # Create hallucination check prompt
            prompt = f"""You are an expert at detecting hallucinations in AI responses.

Question: {question}

Source Documents:
{context}

AI Response:
{generation}

Task: Determine if the AI response is fully grounded in the source documents.
Consider:
1. Are all claims supported by the documents?
2. Is any information added that's not in the sources?
3. Are there any speculative or unsupported statements?

Provide:
1. A binary score ("yes" for grounded, "no" for hallucination)
2. A brief explanation of your decision

Format your response as:
binary_score: [yes/no]
explanation: [your explanation]"""

            # Get structured output
            llm_with_structured_output = self.model.with_structured_output(Grade)
            result = llm_with_structured_output.invoke(prompt)
            
            logger.info(f"Hallucination check result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in hallucination check: {str(e)}")
            return Grade(
                binary_score="no",
                explanation=f"Error during hallucination check: {str(e)}"
            )
    
    def check_answer_relevance(self, question: str, generation: str) -> Grade:
        """
        Check if the generated response actually answers the question.
        
        Args:
            question: Original question
            generation: Generated response
            
        Returns:
            Grade indicating if response answers the question
        """
        try:
            # Create answer relevance prompt
            prompt = f"""You are an expert at evaluating if an answer properly addresses a question.

Question: {question}

Answer:
{generation}

Task: Determine if this answer properly addresses the question.
Consider:
1. Does it directly answer what was asked?
2. Is it complete and clear?
3. Does it stay focused on the question?

Provide:
1. A binary score ("yes" for relevant, "no" for not relevant)
2. A brief explanation of your decision

Format your response as:
binary_score: [yes/no]
explanation: [your explanation]"""

            # Get structured output
            llm_with_structured_output = self.model.with_structured_output(Grade)
            result = llm_with_structured_output.invoke(prompt)
            
            logger.info(f"Answer relevance check result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in answer relevance check: {str(e)}")
            return Grade(
                binary_score="no",
                explanation=f"Error during answer check: {str(e)}"
            )
    
    def suggest_rewrite(self, question: str, failed_retrievals: int = 0) -> str:
        """
        Suggest a rewrite for the question after failed retrievals.
        
        Args:
            question: Original question
            failed_retrievals: Number of failed retrieval attempts
            
        Returns:
            Rewritten question
        """
        try:
            # Create rewrite prompt
            prompt = f"""You are an expert at reformulating questions to improve document retrieval.

Original Question: {question}

This question has failed to retrieve relevant documents {failed_retrievals} time(s).
Please reformulate the question to:
1. Use more general terms if too specific
2. Break down complex questions
3. Use alternative phrasings
4. Focus on key concepts

Provide only the reformulated question without explanation."""

            response = self.model.invoke(prompt)
            rewritten = str(response).strip()
            logger.info(f"Rewrote question: {question} -> {rewritten}")
            return rewritten
            
        except Exception as e:
            logger.error(f"Error in question rewrite: {str(e)}")
            return question  # Return original question on error