"""
Knowledge Retrieval Lab: Vector Databases and Semantic Search
==============================================================

Context Engineering Course - Module 01.2 Laboratory
Building on Context Engineering Survey (arXiv:2507.13334)

This lab provides hands-on experience with vector databases, semantic search,
and knowledge retrieval systems fundamental to modern RAG architectures.

Learning Objectives:
- Understand vector embeddings and semantic similarity
- Implement vector databases from basic principles
- Build production-ready semantic search systems
- Optimize retrieval performance and evaluate effectiveness
- Integrate with broader context engineering frameworks

Usage:
    # For Jupyter/Colab
    %run knowledge_retrieval_lab.py
    
    # For direct execution
    python knowledge_retrieval_lab.py
    
    # For import
    from knowledge_retrieval_lab import *
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
from abc import ABC, abstractmethod
import json
import time
import pickle
import warnings
warnings.filterwarnings('ignore')

# Core imports for embeddings and vector operations
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    print("Warning: sentence-transformers not available. Install with: pip install sentence-transformers")
    SENTENCE_TRANSFORMERS_AVAILABLE = False

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    print("Warning: faiss not available. Install with: pip install faiss-cpu")
    FAISS_AVAILABLE = False

try:
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    print("Warning: scikit-learn not available. Install with: pip install scikit-learn")
    SKLEARN_AVAILABLE = False

# =============================================================================
# SECTION 1: FOUNDATIONAL CONCEPTS
# Vector Spaces and Semantic Similarity
# =============================================================================

def demonstrate_vector_similarity_concepts():
    """
    Demonstrate fundamental concepts of vector similarity and semantic space.
    
    This function illustrates how text can be represented as vectors and how
    semantic similarity translates to geometric proximity in vector space.
    """
    print("=" * 60)
    print("SECTION 1: Vector Similarity Concepts")
    print("=" * 60)
    
    # Simple word vectors for illustration
    word_vectors = {
        'king': np.array([0.8, 0.2, 0.9, 0.1]),
        'queen': np.array([0.7, 0.3, 0.8, 0.2]),
        'man': np.array([0.9, 0.1, 0.3, 0.7]),
        'woman': np.array([0.8, 0.2, 0.2, 0.8]),
        'car': np.array([0.1, 0.9, 0.1, 0.1]),
        'vehicle': np.array([0.2, 0.8, 0.2, 0.1])
    }
    
    def cosine_similarity_manual(vec1, vec2):
        """Calculate cosine similarity manually for educational purposes"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)
    
    print("Word Vector Similarities:")
    print("-" * 30)
    
    # Calculate and display similarities
    similarity_pairs = [
        ('king', 'queen'),
        ('man', 'woman'), 
        ('car', 'vehicle'),
        ('king', 'car'),
        ('queen', 'vehicle')
    ]
    
    for word1, word2 in similarity_pairs:
        similarity = cosine_similarity_manual(word_vectors[word1], word_vectors[word2])
        print(f"{word1:8} ↔ {word2:8}: {similarity:.3f}")
    
    print("\nKey Insights:")
    print("• Related concepts (king/queen, car/vehicle) have higher similarity")
    print("• Unrelated concepts (king/car) have lower similarity")
    print("• Cosine similarity ranges from -1 (opposite) to 1 (identical)")
    
    return word_vectors

@dataclass
class Document:
    """Represents a document with metadata for retrieval systems"""
    id: str
    content: str
    title: str = ""
    metadata: Dict[str, Any] = None
    embedding: Optional[np.ndarray] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class SimpleEmbeddingModel:
    """
    Simple embedding model using TF-IDF for educational purposes.
    
    This implementation helps understand embedding concepts before moving
    to more sophisticated transformer-based models.
    """
    
    def __init__(self, max_features: int = 1000):
        self.max_features = max_features
        self.vectorizer = None
        self.is_fitted = False
        
    def fit(self, documents: List[str]):
        """Fit the embedding model on a corpus of documents"""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn required for SimpleEmbeddingModel")
            
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.vectorizer.fit(documents)
        self.is_fitted = True
        print(f"Model fitted on {len(documents)} documents")
        print(f"Vocabulary size: {len(self.vectorizer.vocabulary_)}")
        
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts into embedding vectors"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before encoding")
            
        embeddings = self.vectorizer.transform(texts).toarray()
        return embeddings
    
    def get_feature_names(self) -> List[str]:
        """Get the feature names (vocabulary) used by the model"""
        if not self.is_fitted:
            return []
        return self.vectorizer.get_feature_names_out().tolist()

# =============================================================================
# SECTION 2: BASIC VECTOR DATABASE IMPLEMENTATION
# Building Understanding Through Implementation
# =============================================================================

class BasicVectorDatabase:
    """
    Basic vector database implementation for educational purposes.
    
    This implementation demonstrates core concepts of vector storage,
    indexing, and similarity search without external dependencies.
    """
    
    def __init__(self, embedding_dim: int):
        self.embedding_dim = embedding_dim
        self.documents: List[Document] = []
        self.embeddings: Optional[np.ndarray] = None
        self.doc_id_to_index: Dict[str, int] = {}
        
    def add_document(self, document: Document, embedding: np.ndarray):
        """Add a document with its embedding to the database"""
        if embedding.shape[0] != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch: expected {self.embedding_dim}, got {embedding.shape[0]}")
        
        # Store document
        doc_index = len(self.documents)
        document.embedding = embedding
        self.documents.append(document)
        self.doc_id_to_index[document.id] = doc_index
        
        # Update embeddings matrix
        if self.embeddings is None:
            self.embeddings = embedding.reshape(1, -1)
        else:
            self.embeddings = np.vstack([self.embeddings, embedding])
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Document, float]]:
        """Search for most similar documents to query embedding"""
        if self.embeddings is None:
            return []
        
        # Calculate cosine similarities
        similarities = self._cosine_similarity_batch(query_embedding, self.embeddings)
        
        # Get top-k results
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            doc = self.documents[idx]
            similarity = similarities[idx]
            results.append((doc, similarity))
        
        return results
    
    def _cosine_similarity_batch(self, query_vec: np.ndarray, doc_vecs: np.ndarray) -> np.ndarray:
        """Efficiently calculate cosine similarity between query and all documents"""
        # Normalize vectors
        query_norm = query_vec / np.linalg.norm(query_vec)
        doc_norms = doc_vecs / np.linalg.norm(doc_vecs, axis=1, keepdims=True)
        
        # Calculate similarities
        similarities = np.dot(doc_norms, query_norm)
        return similarities
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        return {
            'num_documents': len(self.documents),
            'embedding_dimension': self.embedding_dim,
            'total_size_mb': self.embeddings.nbytes / (1024 * 1024) if self.embeddings is not None else 0
        }

def demonstrate_basic_vector_database():
    """Demonstrate basic vector database functionality with sample data"""
    print("\n" + "=" * 60)
    print("SECTION 2: Basic Vector Database Implementation")
    print("=" * 60)
    
    # Sample documents about machine learning
    sample_documents = [
        Document("doc1", "Machine learning is a subset of artificial intelligence that enables computers to learn without being explicitly programmed.", "ML Introduction"),
        Document("doc2", "Deep learning uses neural networks with multiple layers to model and understand complex patterns in data.", "Deep Learning Basics"),
        Document("doc3", "Natural language processing helps computers understand and interpret human language using computational linguistics.", "NLP Overview"),
        Document("doc4", "Computer vision enables machines to interpret and understand visual information from the world.", "Computer Vision"),
        Document("doc5", "Reinforcement learning teaches agents to make decisions through interaction with an environment.", "Reinforcement Learning"),
        Document("doc6", "Data science combines statistics, programming, and domain knowledge to extract insights from data.", "Data Science"),
        Document("doc7", "Neural networks are computing systems inspired by biological neural networks that constitute animal brains.", "Neural Networks"),
        Document("doc8", "Supervised learning uses labeled training data to learn a mapping from inputs to outputs.", "Supervised Learning")
    ]
    
    # Create simple embedding model
    embedding_model = SimpleEmbeddingModel(max_features=500)
    
    # Fit model on document content
    documents_text = [doc.content for doc in sample_documents]
    embedding_model.fit(documents_text)
    
    # Generate embeddings
    embeddings = embedding_model.encode(documents_text)
    
    # Create vector database
    vector_db = BasicVectorDatabase(embedding_dim=embeddings.shape[1])
    
    # Add documents to database
    for doc, embedding in zip(sample_documents, embeddings):
        vector_db.add_document(doc, embedding)
    
    print(f"Created vector database with {len(sample_documents)} documents")
    print(f"Database statistics: {vector_db.get_statistics()}")
    
    # Test queries
    test_queries = [
        "What is artificial intelligence and machine learning?",
        "How do neural networks work?",
        "Understanding human language with computers",
        "Visual recognition and image processing"
    ]
    
    print("\nSearch Results:")
    print("-" * 40)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        
        # Generate query embedding
        query_embedding = embedding_model.encode([query])[0]
        
        # Search database
        results = vector_db.search(query_embedding, top_k=3)
        
        for i, (doc, similarity) in enumerate(results, 1):
            print(f"  {i}. ({similarity:.3f}) {doc.title}")
            print(f"     {doc.content[:100]}...")
    
    return vector_db, embedding_model

# =============================================================================
# SECTION 3: ADVANCED VECTOR DATABASE WITH FAISS
# Professional-Grade Implementation
# =============================================================================

class AdvancedVectorDatabase:
    """
    Advanced vector database using FAISS for high-performance similarity search.
    
    Features:
    - Multiple index types (Flat, IVF, HNSW)
    - Efficient storage and retrieval
    - Metadata filtering
    - Performance optimization
    """
    
    def __init__(self, embedding_dim: int, index_type: str = "Flat"):
        self.embedding_dim = embedding_dim
        self.index_type = index_type
        self.documents: List[Document] = []
        self.doc_id_to_index: Dict[str, int] = {}
        
        if not FAISS_AVAILABLE:
            print("Warning: FAISS not available, falling back to basic implementation")
            self.index = None
            self.use_faiss = False
        else:
            self.index = self._create_faiss_index()
            self.use_faiss = True
    
    def _create_faiss_index(self):
        """Create FAISS index based on specified type"""
        if self.index_type == "Flat":
            return faiss.IndexFlatIP(self.embedding_dim)  # Inner product (cosine similarity)
        elif self.index_type == "IVF":
            quantizer = faiss.IndexFlatIP(self.embedding_dim)
            return faiss.IndexIVFFlat(quantizer, self.embedding_dim, 100)  # 100 clusters
        elif self.index_type == "HNSW":
            return faiss.IndexHNSWFlat(self.embedding_dim, 32)
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")
    
    def add_documents(self, documents: List[Document], embeddings: np.ndarray):
        """Add multiple documents with embeddings efficiently"""
        if embeddings.shape[1] != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch")
        
        start_idx = len(self.documents)
        
        # Add documents to storage
        for i, doc in enumerate(documents):
            doc.embedding = embeddings[i]
            self.documents.append(doc)
            self.doc_id_to_index[doc.id] = start_idx + i
        
        # Normalize embeddings for cosine similarity
        normalized_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        if self.use_faiss:
            # Add to FAISS index
            if self.index_type == "IVF" and not self.index.is_trained:
                self.index.train(normalized_embeddings.astype('float32'))
            
            self.index.add(normalized_embeddings.astype('float32'))
        
        print(f"Added {len(documents)} documents. Total: {len(self.documents)}")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5, 
               filter_metadata: Dict[str, Any] = None) -> List[Tuple[Document, float]]:
        """Search with optional metadata filtering"""
        
        # Normalize query embedding
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        
        if self.use_faiss and len(self.documents) > 0:
            # FAISS search
            scores, indices = self.index.search(
                query_norm.reshape(1, -1).astype('float32'), 
                min(top_k * 2, len(self.documents))  # Get more for filtering
            )
            
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.documents):  # Valid index
                    doc = self.documents[idx]
                    
                    # Apply metadata filtering if specified
                    if filter_metadata:
                        if not self._matches_filter(doc, filter_metadata):
                            continue
                    
                    results.append((doc, float(score)))
                    
                    if len(results) >= top_k:
                        break
        else:
            # Fallback to basic search
            if not self.documents:
                return []
            
            # Calculate similarities manually
            doc_embeddings = np.array([doc.embedding for doc in self.documents])
            doc_norms = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
            similarities = np.dot(doc_norms, query_norm)
            
            # Get top results
            top_indices = np.argsort(similarities)[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                doc = self.documents[idx]
                
                # Apply metadata filtering if specified
                if filter_metadata:
                    if not self._matches_filter(doc, filter_metadata):
                        continue
                
                results.append((doc, similarities[idx]))
        
        return results
    
    def _matches_filter(self, doc: Document, filter_metadata: Dict[str, Any]) -> bool:
        """Check if document matches metadata filter"""
        for key, value in filter_metadata.items():
            if key not in doc.metadata or doc.metadata[key] != value:
                return False
        return True
    
    def save_index(self, filepath: str):
        """Save the vector database to disk"""
        if self.use_faiss:
            faiss.write_index(self.index, f"{filepath}.faiss")
        
        # Save documents and metadata
        with open(f"{filepath}.pkl", 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'doc_id_to_index': self.doc_id_to_index,
                'embedding_dim': self.embedding_dim,
                'index_type': self.index_type
            }, f)
        
        print(f"Saved vector database to {filepath}")
    
    def load_index(self, filepath: str):
        """Load vector database from disk"""
        if self.use_faiss:
            self.index = faiss.read_index(f"{filepath}.faiss")
        
        # Load documents and metadata
        with open(f"{filepath}.pkl", 'rb') as f:
            data = pickle.load(f)
            self.documents = data['documents']
            self.doc_id_to_index = data['doc_id_to_index']
            self.embedding_dim = data['embedding_dim']
            self.index_type = data['index_type']
        
        print(f"Loaded vector database from {filepath}")

# =============================================================================
# SECTION 4: PROFESSIONAL EMBEDDING MODELS
# Transformer-Based Semantic Embeddings
# =============================================================================

class ProfessionalEmbeddingModel:
    """
    Professional embedding model using sentence transformers.
    
    Provides state-of-the-art semantic embeddings for production use.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers required for ProfessionalEmbeddingModel")
        
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded. Embedding dimension: {self.embedding_dim}")
    
    def encode(self, texts: List[str], batch_size: int = 32, show_progress: bool = True) -> np.ndarray:
        """Encode texts into embeddings with batching for efficiency"""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        return embeddings
    
    def encode_single(self, text: str) -> np.ndarray:
        """Encode a single text efficiently"""
        return self.model.encode([text], convert_to_numpy=True)[0]

def demonstrate_professional_embeddings():
    """Demonstrate professional embedding models with real text processing"""
    print("\n" + "=" * 60)
    print("SECTION 3: Professional Embedding Models")
    print("=" * 60)
    
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        print("Skipping professional embeddings demo - sentence-transformers not available")
        return None, None
    
    # Extended document collection covering various AI topics
    documents_data = [
        {"id": "ml_001", "title": "Introduction to Machine Learning", 
         "content": "Machine learning is a method of data analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention.", 
         "category": "machine_learning", "difficulty": "beginner"},
        
        {"id": "dl_001", "title": "Deep Learning Fundamentals",
         "content": "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised, semi-supervised or unsupervised. Deep learning architectures such as deep neural networks, deep belief networks, recurrent neural networks and convolutional neural networks have been applied to fields including computer vision, speech recognition, natural language processing, machine translation, bioinformatics and drug design.",
         "category": "deep_learning", "difficulty": "intermediate"},
        
        {"id": "nlp_001", "title": "Natural Language Processing Overview",
         "content": "Natural language processing is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language, in particular how to program computers to process and analyze large amounts of natural language data. The goal is a computer capable of understanding the contents of documents, including the contextual nuances of the language within them.",
         "category": "nlp", "difficulty": "intermediate"},
        
        {"id": "cv_001", "title": "Computer Vision Applications",
         "content": "Computer vision is an interdisciplinary scientific field that deals with how computers can gain high-level understanding from digital images or videos. From the perspective of engineering, it seeks to understand and automate tasks that the human visual system can do. Computer vision tasks include methods for acquiring, processing, analyzing and understanding digital images.",
         "category": "computer_vision", "difficulty": "intermediate"},
        
        {"id": "rl_001", "title": "Reinforcement Learning Concepts",
         "content": "Reinforcement learning is an area of machine learning concerned with how intelligent agents ought to take actions in an environment in order to maximize the notion of cumulative reward. Reinforcement learning is one of three basic machine learning paradigms, alongside supervised learning and unsupervised learning.",
         "category": "reinforcement_learning", "difficulty": "advanced"},
        
        {"id": "ethics_001", "title": "AI Ethics and Fairness",
         "content": "AI ethics is a set of values, principles, and techniques that employ widely accepted standards of right and wrong to guide moral conduct in the development and use of AI technologies. As AI becomes more prevalent in society, ensuring fairness, accountability, transparency, and human-centered design becomes increasingly important.",
         "category": "ethics", "difficulty": "intermediate"},
        
        {"id": "transformers_001", "title": "Transformer Architecture",
         "content": "The Transformer is a deep learning model introduced in 2017 that uses self-attention mechanisms to process sequential data. It has become the foundation for many state-of-the-art language models including BERT, GPT, and T5. The key innovation is the self-attention mechanism that allows the model to weigh the importance of different parts of the input sequence.",
         "category": "deep_learning", "difficulty": "advanced"},
        
        {"id": "gpt_001", "title": "Generative Pre-trained Transformers",
         "content": "GPT models are a family of neural network models that use the Transformer architecture for natural language processing tasks. They are trained on large amounts of text data to predict the next word in a sequence, which enables them to generate human-like text. GPT models have shown remarkable capabilities in text generation, completion, and various language understanding tasks.",
         "category": "nlp", "difficulty": "advanced"},
        
        {"id": "cnn_001", "title": "Convolutional Neural Networks",
         "content": "Convolutional Neural Networks are a class of deep neural networks most commonly applied to analyzing visual imagery. CNNs use a mathematical operation called convolution in place of general matrix multiplication in at least one of their layers. They are specifically designed to process pixel data and are used in image recognition, medical image analysis, and computer vision applications.",
         "category": "computer_vision", "difficulty": "intermediate"},
        
        {"id": "clustering_001", "title": "Unsupervised Learning and Clustering",
         "content": "Unsupervised learning is a type of machine learning that looks for previously undetected patterns in a data set with no pre-existing labels. Clustering is a common unsupervised learning technique that groups similar data points together. Popular clustering algorithms include K-means, hierarchical clustering, and DBSCAN.",
         "category": "machine_learning", "difficulty": "beginner"}
    ]
    
    # Create documents
    documents = [
        Document(
            id=doc["id"],
            content=doc["content"],
            title=doc["title"],
            metadata={"category": doc["category"], "difficulty": doc["difficulty"]}
        ) for doc in documents_data
    ]
    
    # Initialize professional embedding model
    embedding_model = ProfessionalEmbeddingModel()
    
    # Generate embeddings
    texts = [doc.content for doc in documents]
    print(f"Generating embeddings for {len(documents)} documents...")
    embeddings = embedding_model.encode(texts, show_progress=True)
    
    # Create advanced vector database
    vector_db = AdvancedVectorDatabase(
        embedding_dim=embedding_model.embedding_dim,
        index_type="HNSW" if FAISS_AVAILABLE else "Flat"
    )
    
    # Add documents to database
    vector_db.add_documents(documents, embeddings)
    
    # Test various types of queries
    test_queries = [
        "What are neural networks and how do they work?",
        "Explain computer vision and image processing",
        "How does natural language understanding work?",
        "What is unsupervised machine learning?",
        "Tell me about transformer models and attention mechanisms",
        "What are the ethical considerations in AI development?",
        "How do reinforcement learning agents learn from rewards?"
    ]
    
    print(f"\nSearching with Professional Embeddings:")
    print("-" * 50)
    
    search_results = []
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        
        # Generate query embedding
        query_embedding = embedding_model.encode_single(query)
        
        # Search database
        results = vector_db.search(query_embedding, top_k=3)
        
        query_results = []
        for i, (doc, similarity) in enumerate(results, 1):
            result_info = {
                'rank': i,
                'title': doc.title,
                'similarity': similarity,
                'category': doc.metadata.get('category', 'unknown'),
                'difficulty': doc.metadata.get('difficulty', 'unknown')
            }
            query_results.append(result_info)
            
            print(f"  {i}. ({similarity:.3f}) {doc.title}")
            print(f"     Category: {doc.metadata.get('category', 'N/A')} | "
                  f"Difficulty: {doc.metadata.get('difficulty', 'N/A')}")
        
        search_results.append({
            'query': query,
            'results': query_results
        })
    
    return vector_db, embedding_model, search_results

# =============================================================================
# SECTION 5: RETRIEVAL EVALUATION AND OPTIMIZATION
# Measuring and Improving Search Quality
# =============================================================================

class RetrievalEvaluator:
    """
    Comprehensive evaluation framework for retrieval systems.
    
    Implements standard IR metrics and provides analysis tools for
    understanding and improving retrieval performance.
    """
    
    def __init__(self):
        self.evaluation_results = []
    
    def evaluate_retrieval(self, query: str, retrieved_docs: List[Document], 
                          relevant_doc_ids: List[str], k_values: List[int] = [1, 3, 5, 10]) -> Dict:
        """
        Evaluate retrieval performance using standard metrics.
        
        Args:
            query: The search query
            retrieved_docs: List of retrieved documents in ranking order
            relevant_doc_ids: List of document IDs that are relevant to the query
            k_values: List of k values for precision@k and recall@k evaluation
        
        Returns:
            Dictionary containing evaluation metrics
        """
        retrieved_ids = [doc.id for doc in retrieved_docs]
        relevant_set = set(relevant_doc_ids)
        
        metrics = {
            'query': query,
            'num_relevant': len(relevant_doc_ids),
            'num_retrieved': len(retrieved_docs)
        }
        
        # Calculate precision and recall at different k values
        for k in k_values:
            if k <= len(retrieved_ids):
                retrieved_at_k = set(retrieved_ids[:k])
                relevant_at_k = retrieved_at_k.intersection(relevant_set)
                
                precision_at_k = len(relevant_at_k) / k if k > 0 else 0
                recall_at_k = len(relevant_at_k) / len(relevant_set) if len(relevant_set) > 0 else 0
                
                metrics[f'precision@{k}'] = precision_at_k
                metrics[f'recall@{k}'] = recall_at_k
                
                # F1 score
                if precision_at_k + recall_at_k > 0:
                    f1_at_k = 2 * (precision_at_k * recall_at_k) / (precision_at_k + recall_at_k)
                else:
                    f1_at_k = 0
                metrics[f'f1@{k}'] = f1_at_k
        
        # Mean Average Precision (MAP)
        metrics['average_precision'] = self._calculate_average_precision(retrieved_ids, relevant_set)
        
        # Reciprocal Rank (RR)
        metrics['reciprocal_rank'] = self._calculate_reciprocal_rank(retrieved_ids, relevant_set)
        
        # Normalized Discounted Cumulative Gain (NDCG)
        metrics['ndcg@5'] = self._calculate_ndcg(retrieved_ids, relevant_set, k=5)
        metrics['ndcg@10'] = self._calculate_ndcg(retrieved_ids, relevant_set, k=10)
        
        self.evaluation_results.append(metrics)
        return metrics
    
    def _calculate_average_precision(self, retrieved_ids: List[str], relevant_set: set) -> float:
        """Calculate Average Precision for a single query"""
        if not relevant_set:
            return 0.0
        
        relevant_count = 0
        precision_sum = 0.0
        
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant_set:
                relevant_count += 1
                precision_at_i = relevant_count / (i + 1)
                precision_sum += precision_at_i
        
        return precision_sum / len(relevant_set) if len(relevant_set) > 0 else 0.0
    
    def _calculate_reciprocal_rank(self, retrieved_ids: List[str], relevant_set: set) -> float:
        """Calculate Reciprocal Rank - position of first relevant document"""
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant_set:
                return 1.0 / (i + 1)
        return 0.0
    
    def _calculate_ndcg(self, retrieved_ids: List[str], relevant_set: set, k: int) -> float:
        """Calculate Normalized Discounted Cumulative Gain at k"""
        def dcg(relevances: List[int], k: int) -> float:
            dcg_score = 0.0
            for i in range(min(k, len(relevances))):
                dcg_score += relevances[i] / np.log2(i + 2)
            return dcg_score
        
        # Actual relevances (1 if relevant, 0 if not)
        actual_relevances = [1 if doc_id in relevant_set else 0 for doc_id in retrieved_ids[:k]]
        
        # Ideal relevances (all 1s up to number of relevant docs)
        ideal_relevances = [1] * min(k, len(relevant_set)) + [0] * max(0, k - len(relevant_set))
        
        actual_dcg = dcg(actual_relevances, k)
        ideal_dcg = dcg(ideal_relevances, k)
        
        return actual_dcg / ideal_dcg if ideal_dcg > 0 else 0.0
    
    def get_summary_statistics(self) -> Dict:
        """Get summary statistics across all evaluated queries"""
        if not self.evaluation_results:
            return {}
        
        # Aggregate metrics
        metrics_to_aggregate = [
            'precision@1', 'precision@3', 'precision@5', 'precision@10',
            'recall@1', 'recall@3', 'recall@5', 'recall@10',
            'f1@1', 'f1@3', 'f1@5', 'f1@10',
            'average_precision', 'reciprocal_rank', 'ndcg@5', 'ndcg@10'
        ]
        
        summary = {}
        for metric in metrics_to_aggregate:
            values = [result[metric] for result in self.evaluation_results if metric in result]
            if values:
                summary[f'mean_{metric}'] = np.mean(values)
                summary[f'std_{metric}'] = np.std(values)
        
        # Mean Average Precision (MAP) - average of average precisions
        map_score = np.mean([result['average_precision'] for result in self.evaluation_results])
        summary['MAP'] = map_score
        
        # Mean Reciprocal Rank (MRR)
        mrr_score = np.mean([result['reciprocal_rank'] for result in self.evaluation_results])
        summary['MRR'] = mrr_score
        
        return summary

def create_evaluation_dataset():
    """
    Create a synthetic evaluation dataset with ground truth relevance judgments.
    
    In practice, this would come from human annotations or existing benchmark datasets.
    """
    # Define test queries and their relevant documents
    evaluation_data = [
        {
            'query': 'What are neural networks and how do they work?',
            'relevant_docs': ['dl_001', 'transformers_001', 'cnn_001']  # Deep learning related
        },
        {
            'query': 'Explain computer vision and image processing',
            'relevant_docs': ['cv_001', 'cnn_001']  # Computer vision specific
        },
        {
            'query': 'How does natural language understanding work?',
            'relevant_docs': ['nlp_001', 'gpt_001', 'transformers_001']  # NLP related
        },
        {
            'query': 'What is unsupervised machine learning?',
            'relevant_docs': ['clustering_001', 'ml_001']  # Unsupervised learning
        },
        {
            'query': 'Tell me about transformer models',
            'relevant_docs': ['transformers_001', 'gpt_001']  # Transformer specific
        },
        {
            'query': 'What are the ethical considerations in AI?',
            'relevant_docs': ['ethics_001']  # Ethics specific
        },
        {
            'query': 'How do agents learn from rewards?',
            'relevant_docs': ['rl_001']  # Reinforcement learning specific
        }
    ]
    
    return evaluation_data

def demonstrate_retrieval_evaluation(vector_db, embedding_model):
    """Demonstrate comprehensive retrieval evaluation"""
    print("\n" + "=" * 60)
    print("SECTION 4: Retrieval Evaluation and Optimization")
    print("=" * 60)
    
    if vector_db is None or embedding_model is None:
        print("Skipping evaluation demo - vector database not available")
        return None
    
    # Create evaluation dataset
    evaluation_data = create_evaluation_dataset()
    
    # Initialize evaluator
    evaluator = RetrievalEvaluator()
    
    print(f"Evaluating retrieval system on {len(evaluation_data)} test queries...")
    print("-" * 50)
    
    # Evaluate each query
    for test_case in evaluation_data:
        query = test_case['query']
        relevant_doc_ids = test_case['relevant_docs']
        
        # Generate query embedding and search
        query_embedding = embedding_model.encode_single(query)
        results = vector_db.search(query_embedding, top_k=10)
        retrieved_docs = [doc for doc, score in results]
        
        # Evaluate
        metrics = evaluator.evaluate_retrieval(query, retrieved_docs, relevant_doc_ids)
        
        print(f"Query: {query}")
        print(f"  Relevant docs: {len(relevant_doc_ids)}")
        print(f"  Precision@3: {metrics['precision@3']:.3f}")
        print(f"  Recall@3: {metrics['recall@3']:.3f}")
        print(f"  Average Precision: {metrics['average_precision']:.3f}")
        print(f"  Reciprocal Rank: {metrics['reciprocal_rank']:.3f}")
        print()
    
    # Get summary statistics
    summary = evaluator.get_summary_statistics()
    
    print("Overall Performance Summary:")
    print("-" * 30)
    print(f"Mean Average Precision (MAP): {summary['MAP']:.3f}")
    print(f"Mean Reciprocal Rank (MRR): {summary['MRR']:.3f}")
    print(f"Mean Precision@3: {summary['mean_precision@3']:.3f}")
    print(f"Mean Recall@3: {summary['mean_recall@3']:.3f}")
    print(f"Mean NDCG@5: {summary['mean_ndcg@5']:.3f}")
    
    return evaluator, summary

# =============================================================================
# SECTION 6: PERFORMANCE OPTIMIZATION AND BENCHMARKING
# Making Retrieval Fast and Scalable
# =============================================================================

class PerformanceBenchmark:
    """
    Comprehensive performance benchmarking for vector databases.
    
    Measures search latency, indexing time, memory usage, and scalability.
    """
    
    def __init__(self):
        self.benchmark_results = []
    
    def benchmark_search_performance(self, vector_db, embedding_model, 
                                   num_queries: int = 100) -> Dict:
        """Benchmark search performance with multiple queries"""
        print(f"Benchmarking search performance with {num_queries} queries...")
        
        # Generate random queries (in practice, use realistic query distribution)
        sample_queries = [
            "machine learning algorithms",
            "neural network architectures", 
            "computer vision applications",
            "natural language processing",
            "deep learning models",
            "artificial intelligence ethics",
            "reinforcement learning agents",
            "transformer models",
            "unsupervised learning methods",
            "data science techniques"
        ]
        
        search_times = []
        embedding_times = []
        
        for i in range(num_queries):
            query = sample_queries[i % len(sample_queries)]
            
            # Time embedding generation
            start_time = time.time()
            query_embedding = embedding_model.encode_single(query)
            embedding_time = time.time() - start_time
            embedding_times.append(embedding_time)
            
            # Time search
            start_time = time.time()
            results = vector_db.search(query_embedding, top_k=10)
            search_time = time.time() - start_time
            search_times.append(search_time)
        
        # Calculate statistics
        results = {
            'num_queries': num_queries,
            'mean_search_time': np.mean(search_times),
            'std_search_time': np.std(search_times),
            'mean_embedding_time': np.mean(embedding_times),
            'std_embedding_time': np.std(embedding_times),
            'p95_search_time': np.percentile(search_times, 95),
            'p99_search_time': np.percentile(search_times, 99),
            'total_time': np.sum(search_times) + np.sum(embedding_times),
            'queries_per_second': num_queries / (np.sum(search_times) + np.sum(embedding_times))
        }
        
        self.benchmark_results.append(results)
        return results
    
    def benchmark_scalability(self, embedding_model, doc_counts: List[int] = [100, 500, 1000, 2000]):
        """Benchmark how performance scales with database size"""
        print("Benchmarking scalability across different database sizes...")
        
        scalability_results = []
        
        for doc_count in doc_counts:
            print(f"  Testing with {doc_count} documents...")
            
            # Generate synthetic documents
            synthetic_docs = []
            for i in range(doc_count):
                content = f"This is synthetic document {i} about artificial intelligence and machine learning topics. " \
                         f"It contains information about neural networks, deep learning, and data science applications."
                doc = Document(f"synthetic_{i}", content, f"Synthetic Doc {i}")
                synthetic_docs.append(doc)
            
            # Generate embeddings
            texts = [doc.content for doc in synthetic_docs]
            start_time = time.time()
            embeddings = embedding_model.encode(texts, show_progress=False)
            embedding_time = time.time() - start_time
            
            # Create database
            vector_db = AdvancedVectorDatabase(
                embedding_dim=embedding_model.embedding_dim,
                index_type="Flat"  # Use simple index for consistent comparison
            )
            
            # Time database construction
            start_time = time.time()
            vector_db.add_documents(synthetic_docs, embeddings)
            construction_time = time.time() - start_time
            
            # Benchmark search performance
            search_benchmark = self.benchmark_search_performance(vector_db, embedding_model, num_queries=50)
            
            scalability_results.append({
                'doc_count': doc_count,
                'embedding_time': embedding_time,
                'construction_time': construction_time,
                'mean_search_time': search_benchmark['mean_search_time'],
                'queries_per_second': search_benchmark['queries_per_second']
            })
        
        return scalability_results
    
    def plot_performance_results(self, scalability_results):
        """Visualize performance benchmarking results"""
        if not scalability_results:
            print("No scalability results to plot")
            return
        
        df = pd.DataFrame(scalability_results)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Search time vs database size
        axes[0, 0].plot(df['doc_count'], df['mean_search_time'] * 1000, 'b-o')
        axes[0, 0].set_xlabel('Number of Documents')
        axes[0, 0].set_ylabel('Mean Search Time (ms)')
        axes[0, 0].set_title('Search Latency vs Database Size')
        axes[0, 0].grid(True)
        
        # Queries per second vs database size
        axes[0, 1].plot(df['doc_count'], df['queries_per_second'], 'r-o')
        axes[0, 1].set_xlabel('Number of Documents')
        axes[0, 1].set_ylabel('Queries per Second')
        axes[0, 1].set_title('Throughput vs Database Size')
        axes[0, 1].grid(True)
        
        # Construction time vs database size
        axes[1, 0].plot(df['doc_count'], df['construction_time'], 'g-o')
        axes[1, 0].set_xlabel('Number of Documents')
        axes[1, 0].set_ylabel('Index Construction Time (s)')
        axes[1, 0].set_title('Index Construction vs Database Size')
        axes[1, 0].grid(True)
        
        # Embedding time vs database size
        axes[1, 1].plot(df['doc_count'], df['embedding_time'], 'm-o')
        axes[1, 1].set_xlabel('Number of Documents')
        axes[1, 1].set_ylabel('Embedding Generation Time (s)')
        axes[1, 1].set_title('Embedding Time vs Database Size')
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.show()
        
        return fig

def demonstrate_performance_optimization(vector_db, embedding_model):
    """Demonstrate performance optimization techniques"""
    print("\n" + "=" * 60)
    print("SECTION 5: Performance Optimization")
    print("=" * 60)
    
    if vector_db is None or embedding_model is None:
        print("Skipping performance demo - vector database not available")
        return None
    
    # Initialize benchmark suite
    benchmark = PerformanceBenchmark()
    
    # Benchmark current system
    print("Benchmarking current system performance...")
    search_results = benchmark.benchmark_search_performance(vector_db, embedding_model, num_queries=50)
    
    print("Search Performance Results:")
    print(f"  Mean search time: {search_results['mean_search_time']*1000:.2f} ms")
    print(f"  Mean embedding time: {search_results['mean_embedding_time']*1000:.2f} ms")
    print(f"  95th percentile search time: {search_results['p95_search_time']*1000:.2f} ms")
    print(f"  Queries per second: {search_results['queries_per_second']:.1f}")
    
    # Scalability analysis (reduced for demo purposes)
    print("\nRunning scalability analysis...")
    scalability_results = benchmark.benchmark_scalability(
        embedding_model, 
        doc_counts=[50, 100, 200]  # Reduced for demo
    )
    
    print("\nScalability Results:")
    for result in scalability_results:
        print(f"  {result['doc_count']} docs: "
              f"{result['mean_search_time']*1000:.2f}ms search, "
              f"{result['queries_per_second']:.1f} QPS")
    
    # Performance optimization recommendations
    print("\nPerformance Optimization Recommendations:")
    print("-" * 40)
    
    recommendations = []
    
    if search_results['mean_search_time'] > 0.1:  # > 100ms
        recommendations.append("Consider using approximate search (IVF or HNSW index)")
    
    if search_results['mean_embedding_time'] > 0.05:  # > 50ms
        recommendations.append("Consider batching queries or using GPU acceleration")
    
    if not recommendations:
        recommendations.append("Performance is good - consider monitoring at scale")
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    
    # Plot results if matplotlib available
    try:
        benchmark.plot_performance_results(scalability_results)
    except Exception as e:
        print(f"Could not generate plots: {e}")
    
    return benchmark, scalability_results

# =============================================================================
# MAIN EXECUTION AND DEMONSTRATION
# Complete Lab Workflow
# =============================================================================

def run_complete_lab():
    """
    Run the complete knowledge retrieval lab demonstration.
    
    This function orchestrates all sections of the lab, providing a
    comprehensive learning experience in vector databases and semantic search.
    """
    print("Knowledge Retrieval Lab: Vector Databases and Semantic Search")
    print("=" * 70)
    print("Context Engineering Course - Module 01.2 Laboratory")
    print("Building on Context Engineering Survey (arXiv:2507.13334)")
    print("=" * 70)
    
    # Section 1: Foundational concepts
    word_vectors = demonstrate_vector_similarity_concepts()
    
    # Section 2: Basic implementation
    basic_db, simple_model = demonstrate_basic_vector_database()
    
    # Section 3: Professional implementation
    vector_db, embedding_model, search_results = demonstrate_professional_embeddings()
    
    # Section 4: Evaluation
    evaluator, eval_summary = demonstrate_retrieval_evaluation(vector_db, embedding_model)
    
    # Section 5: Performance optimization
    benchmark, scalability_results = demonstrate_performance_optimization(vector_db, embedding_model)
    
    # Final summary
    print("\n" + "=" * 70)
    print("LAB COMPLETION SUMMARY")
    print("=" * 70)
    
    print("Concepts Covered:")
    print("• Vector embeddings and semantic similarity")
    print("• Basic vector database implementation")
    print("• Professional-grade semantic search systems")
    print("• Retrieval evaluation and metrics")
    print("• Performance optimization and scalability")
    
    if eval_summary:
        print(f"\nSystem Performance:")
        print(f"• Mean Average Precision (MAP): {eval_summary['MAP']:.3f}")
        print(f"• Mean Reciprocal Rank (MRR): {eval_summary['MRR']:.3f}")
        print(f"• Mean Precision@3: {eval_summary['mean_precision@3']:.3f}")
    
    if benchmark and benchmark.benchmark_results:
        latest_perf = benchmark.benchmark_results[-1]
        print(f"• Average search latency: {latest_perf['mean_search_time']*1000:.1f}ms")
        print(f"• Throughput: {latest_perf['queries_per_second']:.1f} queries/second")
    
    print("\nNext Steps:")
    print("• Experiment with different embedding models")
    print("• Try different FAISS index types for your use case")
    print("• Implement custom similarity metrics")
    print("• Integrate with real-world document collections")
    print("• Explore hybrid search combining dense and sparse retrieval")
    
    return {
        'basic_db': basic_db,
        'vector_db': vector_db,
        'embedding_model': embedding_model,
        'evaluator': evaluator,
        'benchmark': benchmark,
        'search_results': search_results
    }

# =============================================================================
# UTILITY FUNCTIONS FOR JUPYTER/COLAB INTEGRATION
# =============================================================================

def setup_lab_environment():
    """Setup function for Jupyter/Colab environments"""
    print("Setting up Knowledge Retrieval Lab environment...")
    
    # Check and install requirements
    required_packages = [
        'sentence-transformers',
        'faiss-cpu', 
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'pandas'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing packages detected. Please install:")
        print("pip install " + " ".join(missing_packages))
        return False
    
    print("Environment setup complete!")
    return True

def quick_demo():
    """Quick demonstration for time-constrained environments"""
    print("Quick Knowledge Retrieval Demo")
    print("=" * 40)
    
    # Run essential sections only
    demonstrate_vector_similarity_concepts()
    basic_db, simple_model = demonstrate_basic_vector_database()
    
    return basic_db, simple_model

def interactive_search_demo(vector_db, embedding_model):
    """Interactive search interface for experimentation"""
    if vector_db is None or embedding_model is None:
        print("Vector database not available for interactive demo")
        return
    
    print("Interactive Search Demo")
    print("Enter queries to search the knowledge base (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        try:
            query = input("\nEnter your query: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if not query:
                continue
            
            # Perform search
            query_embedding = embedding_model.encode_single(query)
            results = vector_db.search(query_embedding, top_k=3)
            
            print(f"\nResults for: '{query}'")
            print("-" * 30)
            
            for i, (doc, similarity) in enumerate(results, 1):
                print(f"{i}. ({similarity:.3f}) {doc.title}")
                print(f"   {doc.content[:100]}...")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("Interactive demo ended.")

# Entry point for direct execution
if __name__ == "__main__":
    # Run the complete lab
    lab_results = run_complete_lab()
    
    # Optional: Start interactive demo
    print("\nWould you like to try the interactive search demo? (y/n)")
    try:
        response = input().strip().lower()
        if response == 'y':
            interactive_search_demo(
                lab_results['vector_db'], 
                lab_results['embedding_model']
            )
    except:
        print("Interactive demo skipped.")
    
    print("\nLab completed successfully!")
