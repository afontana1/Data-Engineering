import os
from typing import Dict, List, Tuple
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

class TopicDetector:
    def __init__(self, topics: Dict[str, List[str]]):
        """
        Initialize the topic detector with topic descriptions.
        
        Args:
            topics: Dictionary mapping topic names to lists of example queries/descriptions
        """
        self.topics = topics
        self.topic_embeddings = self._get_topic_embeddings()
    
    def _get_topic_embeddings(self) -> Dict[str, List[float]]:
        """Get embeddings for all topic descriptions."""
        embeddings = {}
        for topic, descriptions in self.topics.items():
            # Combine all descriptions for the topic
            combined_text = " ".join(descriptions)
            # Get embedding for the combined text
            response = openai.embeddings.create(
                model="text-embedding-3-small",
                input=combined_text
            )
            embeddings[topic] = response.data[0].embedding
        return embeddings
    
    def detect_topic(self, message: str) -> Tuple[str, float]:
        """
        Detect the topic of a message using embeddings similarity.
        
        Args:
            message: The message to classify
            
        Returns:
            Tuple of (detected_topic, confidence_score)
        """
        # Get embedding for the message
        response = openai.embeddings.create(
            model="text-embedding-3-small",
            input=message
        )
        message_embedding = response.data[0].embedding
        
        # Calculate similarity with each topic
        similarities = {}
        for topic, topic_embedding in self.topic_embeddings.items():
            similarity = self._cosine_similarity(message_embedding, topic_embedding)
            similarities[topic] = similarity
        
        # Get the topic with highest similarity
        best_topic = max(similarities.items(), key=lambda x: x[1])
        return best_topic
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (norm1 * norm2) 