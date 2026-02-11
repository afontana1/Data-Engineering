# Reranking in RAG Systems

> **Implementation File**: [`src/reranking_rag_systems.py`](../src/reranking_rag_systems.py)
> 
> **Production-ready implementation** with support for Cohere, SentenceTransformer, and LLM reranking, ensemble methods, caching, and comprehensive evaluation capabilities.

## Overview

Reranking is a post-processing technique that improves retrieval quality by re-evaluating and re-ordering initial search results. It acts as a second-pass filter to ensure the most relevant context is provided to the LLM.

Our implementation provides a unified interface for different reranking approaches through the `RerankerManager` class, with advanced features like ensemble reranking and performance optimization.

## Quick Start (3 minutes)

Get reranking working immediately with our production-ready implementation:

```python
from src.reranking_rag_systems import RerankerConfig, RerankerManager

# 1. Configure your reranker
config = RerankerConfig(
    reranker_type="cohere",  # or "sentence_transformer", "llm"
    top_k=5,
    api_key="your-cohere-api-key",  # Only needed for Cohere
    use_cache=True  # Enable caching for better performance
)

# 2. Initialize reranker manager
reranker = RerankerManager(config)

# 3. Rerank your documents
documents = [
    {"id": 1, "text": "Document about machine learning"},
    {"id": 2, "text": "Document about data science"},
    {"id": 3, "text": "Document about cooking recipes"}
]

results = reranker.rerank_results(
    query="What is machine learning?",
    documents=documents
)

print(f"Top reranked result: {results[0]}")
```

## Module Overview

### Core Classes

#### `RerankerConfig` (dataclass)
Configuration class for reranker setup:
- `reranker_type`: Type of reranker ('cohere', 'sentence_transformer', 'llm')
- `top_k`: Number of results to return (default: 5)
- `model_name`: Specific model to use (optional)
- `api_key`: API key for external services (optional)
- `threshold`: Minimum relevance score (default: 0.0)
- `use_cache`: Enable result caching (default: True)

#### `RerankerManager`
Main class managing reranking operations:
- `__init__(config)`: Initialize with RerankerConfig
- `rerank_results(query, documents)`: Core reranking method
- `evaluate_reranker(eval_dataset)`: Evaluate reranker performance
- `_initialize_reranker()`: Set up appropriate reranker type

#### `EnsembleReranker`
Advanced ensemble reranking combining multiple approaches:
- `__init__(rerankers, weights)`: Initialize with multiple RerankerManagers
- `rerank(query, documents)`: Combine results with weighted scoring

## Reranker Types

### 1. Cohere Rerank
Production-ready reranking service with state-of-the-art performance:

```python
from src.reranking_rag_systems import RerankerConfig, RerankerManager

# Configure Cohere reranker
config = RerankerConfig(
    reranker_type="cohere",
    top_k=5,
    api_key="your-cohere-api-key",
    model_name="rerank-english-v2.0"  # or "rerank-multilingual-v2.0"
)

cohere_reranker = RerankerManager(config)
```

**Features:**
- Optimized for semantic similarity
- Supports multiple languages
- Provides confidence scores
- Enterprise-grade reliability

### 2. SentenceTransformer Rerank
Local implementation using cross-encoder models:

```python
# Configure SentenceTransformer reranker
config = RerankerConfig(
    reranker_type="sentence_transformer",
    top_k=5,
    model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
    threshold=0.3  # Filter low-confidence results
)

st_reranker = RerankerManager(config)
```

**Features:**
- Runs locally (no API calls)
- Customizable for specific domains
- Multiple pre-trained models available
- Cost-effective for high-volume usage

### 3. LLM Rerank
Uses language models for context-aware reranking:

```python
# Configure LLM reranker
config = RerankerConfig(
    reranker_type="llm",
    top_k=5
)

llm_reranker = RerankerManager(config)
```

**Features:**
- Highly flexible ranking criteria
- Can understand complex queries
- Contextual relevance assessment
- Best for nuanced relevance needs

## Advanced Usage

### Ensemble Reranking

Combine multiple rerankers for optimal results using the `EnsembleReranker` class:

```python
from src.reranking_rag_systems import EnsembleReranker

# Set up individual rerankers
cohere_config = RerankerConfig(
    reranker_type="cohere",
    top_k=10,
    api_key="your-api-key"
)

st_config = RerankerConfig(
    reranker_type="sentence_transformer",
    top_k=10
)

cohere_reranker = RerankerManager(cohere_config)
st_reranker = RerankerManager(st_config)

# Create ensemble with weighted combination
ensemble = EnsembleReranker(
    rerankers=[cohere_reranker, st_reranker],
    weights=[0.7, 0.3]  # 70% Cohere, 30% SentenceTransformer
)

# Use ensemble reranker
results = ensemble.rerank(query="your query", documents=documents)
```

### Performance Optimization

Our implementation includes several performance optimizations:

#### Caching (LRU Cache)
```python
# Caching is enabled by default and uses @lru_cache decorator
# See _cached_rerank() method in RerankerManager (line 64-67)
config = RerankerConfig(
    reranker_type="cohere",
    use_cache=True  # Default: True
)
```

#### Threshold Filtering
```python
config = RerankerConfig(
    reranker_type="sentence_transformer",
    threshold=0.5,  # Only return results with score >= 0.5
    top_k=10
)
```

### Evaluation and Monitoring

Evaluate your reranker's performance using built-in evaluation methods:

```python
async def evaluate_reranking_performance():
    # Initialize reranker
    reranker = RerankerManager(your_config)
    
    # Run evaluation (uses RetrieverEvaluator)
    metrics = await reranker.evaluate_reranker(eval_dataset)
    
    print(f"MRR: {metrics['mrr']:.3f}")
    print(f"Hit Rate: {metrics['hit_rate']:.3f}")

# The evaluate_reranker() method computes:
# - Mean Reciprocal Rank (MRR)
# - Hit Rate
# See lines 98-121 in implementation
```

## Integration Patterns

### Two-Stage RAG Pipeline

Implement efficient two-stage retrieval with reranking:

```python
# Stage 1: Retrieve more candidates
initial_retriever = index.as_retriever(similarity_top_k=20)
initial_results = initial_retriever.retrieve(query)

# Stage 2: Rerank to get best matches
reranker = RerankerManager(RerankerConfig(
    reranker_type="cohere",
    top_k=5,
    api_key="your-api-key"
))

final_results = reranker.rerank_results(query, initial_results)
```

### Query Engine Integration

Integrate with LlamaIndex query engines:

```python
from llama_index.postprocessor.cohere_rerank import CohereRerank

# Use with existing LlamaIndex components
reranker = CohereRerank(
    api_key="your-api-key",
    top_n=5,
    model="rerank-english-v2.0"
)

query_engine = index.as_query_engine(
    similarity_top_k=10,
    node_postprocessors=[reranker]
)
```

## Configuration Reference

### Complete Configuration Options

```python
config = RerankerConfig(
    reranker_type="cohere",           # Required: 'cohere', 'sentence_transformer', 'llm'
    top_k=5,                         # Number of results to return
    model_name="rerank-english-v2.0", # Model to use (optional)
    api_key="your-api-key",          # Required for Cohere
    threshold=0.0,                   # Minimum relevance score
    use_cache=True                   # Enable LRU caching
)
```

### Model Options

#### Cohere Models
- `rerank-english-v2.0`: English-optimized model
- `rerank-multilingual-v2.0`: Multi-language support

#### SentenceTransformer Models
- `cross-encoder/ms-marco-MiniLM-L-6-v2`: General purpose (default)
- `cross-encoder/ms-marco-MiniLM-L-12-v2`: Higher accuracy
- `cross-encoder/stsb-distilbert-base`: Semantic similarity focused

## Performance Considerations

### Latency Optimization
- **Caching**: Enabled by default (`use_cache=True`)
- **Batch Processing**: Process multiple queries together
- **Threshold Filtering**: Reduce processing of low-relevance results

### Cost Management
- **Local Models**: Use SentenceTransformer for cost-effective processing
- **API Rate Limiting**: Implement delays for API-based rerankers
- **Selective Reranking**: Only rerank when necessary

### Quality Tuning
- **Threshold Adjustment**: Filter low-confidence results
- **Model Selection**: Choose appropriate model for your domain
- **Ensemble Weights**: Balance different reranker strengths

## Troubleshooting

### Common Issues and Solutions

#### 1. Poor Reranking Results
```python
# Check input quality and adjust parameters
config = RerankerConfig(
    reranker_type="cohere",
    top_k=10,  # Increase to see more results
    threshold=0.2,  # Lower threshold for more inclusive results
)
```

#### 2. Performance Bottlenecks
```python
# Enable caching and optimize batch sizes
config = RerankerConfig(
    reranker_type="sentence_transformer",
    use_cache=True,  # Enable caching
    top_k=5  # Reduce processing load
)
```

#### 3. API Key Issues
```python
# Ensure proper API key configuration
config = RerankerConfig(
    reranker_type="cohere",
    api_key="co-your-actual-api-key-here"  # Check API key format
)
```

## Source Code Exploration

### Key Methods to Explore

1. **`_initialize_reranker()`** (lines 36-62): See how different reranker types are instantiated
2. **`rerank_results()`** (lines 69-96): Core reranking logic with caching and filtering  
3. **`_cached_rerank()`** (lines 64-67): LRU cache implementation for performance
4. **`evaluate_reranker()`** (lines 98-121): Evaluation framework using MRR and hit rate
5. **`EnsembleReranker.rerank()`** (lines 134-158): Weighted ensemble combination logic

### Extension Points

The implementation is designed for easy extension:

- **Add New Reranker Types**: Extend `_initialize_reranker()` method
- **Custom Evaluation Metrics**: Modify `evaluate_reranker()` method  
- **Enhanced Caching**: Customize `_cached_rerank()` behavior
- **Advanced Ensemble Logic**: Extend `EnsembleReranker` class

## Quick Reference

| Class/Method | Purpose | Key Parameters |
|--------------|---------|----------------|
| `RerankerConfig` | Configuration setup | `reranker_type`, `top_k`, `api_key` |
| `RerankerManager` | Main reranking operations | `config: RerankerConfig` |
| `rerank_results()` | Core reranking method | `query: str`, `documents: List[Any]` |
| `EnsembleReranker` | Multi-reranker combination | `rerankers: List`, `weights: List` |
| `evaluate_reranker()` | Performance evaluation | `eval_dataset` |
| `example_usage()` | Complete usage example | See lines 161-203 |

## Best Practices

### 1. Production Deployment
- Use caching for repeated queries
- Implement proper error handling
- Monitor reranking latency and costs
- Set appropriate relevance thresholds

### 2. Model Selection
- **Cohere**: Production applications requiring high accuracy
- **SentenceTransformer**: Cost-sensitive or privacy-focused deployments  
- **LLM**: Complex relevance criteria or specialized domains

### 3. Performance Tuning
- Start with default configurations
- Adjust `top_k` based on downstream requirements
- Use ensemble methods for critical applications
- Monitor evaluation metrics regularly

The implementation provides a complete, production-ready reranking solution that balances performance, flexibility, and ease of use. Explore the source code to understand the implementation details and customize for your specific needs.