# RAG Metrics & Evaluation: Comprehensive Guide

> **📁 Implementation File**: [`src/rag_metrics_evaluation_module.py`](../src/rag_metrics_evaluation_module.py)  
> **🎯 Main Class**: `RAGEvaluationFramework`  
> **⚙️ Configuration**: `EvaluationConfig`

## Table of Contents
1. [Quick Start](#quick-start)
2. [Module Overview](#module-overview)
3. [Introduction](#introduction)
4. [Understanding RAG Evaluation](#understanding-rag-evaluation)
5. [Evaluation Metrics Explained](#evaluation-metrics-explained)
6. [Environment Setup](#environment-setup)
7. [Step-by-Step Implementation](#step-by-step-implementation)
8. [Advanced Evaluation Techniques](#advanced-evaluation-techniques)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [Practical Examples](#practical-examples)

## Quick Start

Ready to evaluate your RAG system? Here's how to get started in 3 minutes:

```python
# Import our evaluation framework
from src.rag_metrics_evaluation_module import RAGEvaluationFramework, EvaluationConfig
import asyncio

# 1. Configure evaluation (see EvaluationConfig class for all options)
config = EvaluationConfig(
    llm_model="gpt-3.5-turbo",
    chunk_size=512,
    enable_ragas=True
)

# 2. Initialize evaluator (see RAGEvaluationFramework.__init__)
evaluator = RAGEvaluationFramework(config)

# 3. Run comprehensive evaluation (see comprehensive_evaluation method)
results = asyncio.run(
    evaluator.comprehensive_evaluation(documents_path="your/documents/path")
)

print("Your RAG system scores:")
print(f"📊 Retrieval MRR: {results['retrieval_metrics']['mrr']:.3f}")
print(f"✅ Faithfulness: {results['generation_metrics']['faithfulness']:.3f}")
print(f"🎯 Relevancy: {results['generation_metrics']['relevancy']:.3f}")
```

## Module Overview

Our implementation is contained in **`src/rag_metrics_evaluation_module.py`** and provides:

### 🏗️ Core Classes

#### `EvaluationConfig` (Dataclass)
Configuration object for all evaluation settings:
- **LLM Configuration**: Model selection, temperature settings
- **Chunking Strategy**: Chunk size, overlap, retrieval parameters  
- **Evaluation Options**: RAGAS enablement, metrics selection
- **Performance Tuning**: Batch size, workers, caching options

#### `RAGEvaluationFramework` (Main Class)
The central evaluation engine with key methods:
- **`setup_vector_store()`**: Initialize vector stores and indices
- **`generate_evaluation_dataset()`**: Create evaluation queries automatically
- **`evaluate_retrieval_performance()`**: Assess retrieval quality (MRR, Hit Rate)
- **`evaluate_generation_quality()`**: Measure response quality (Faithfulness, Relevancy)
- **`evaluate_with_ragas()`**: Run RAGAS comprehensive metrics
- **`comprehensive_evaluation()`**: Execute all evaluations in one call
- **`compare_llm_performance()`**: A/B test different models
- **`export_results()`**: Export results to pandas/JSON

### 🔧 Key Features Implemented
- **Async Support**: Non-blocking evaluation for better performance
- **Batch Processing**: Efficient handling of large evaluation datasets
- **Multiple Vector Stores**: Support for simple and DeepLake stores
- **Comprehensive Metrics**: Both LlamaIndex and RAGAS frameworks
- **Error Handling**: Robust exception handling and logging
- **Export Capabilities**: Results in multiple formats

## Introduction

Evaluation is a critical component of any RAG (Retrieval-Augmented Generation) system. Without proper evaluation, it's impossible to know if your RAG system is performing well, which components need improvement, or how changes affect overall performance.

This guide provides a comprehensive approach to RAG evaluation using our **`RAGEvaluationFramework`** class, which integrates two powerful frameworks:
- **LlamaIndex**: Provides built-in evaluators for retrieval and generation quality
- **RAGAS**: Offers comprehensive metrics specifically designed for RAG systems

### Why RAG Evaluation Matters

RAG systems are complex pipelines involving multiple components:
- **Document Processing**: Chunking, embedding generation
- **Retrieval**: Finding relevant context from vector stores
- **Generation**: Creating responses using retrieved context
- **Post-processing**: Formatting and filtering responses

Each component can affect the overall system performance, making evaluation essential for:
- **Quality Assurance**: Ensuring responses are accurate and relevant
- **Performance Optimization**: Identifying bottlenecks and improvement areas
- **Model Comparison**: Choosing the best LLM or embedding model
- **System Monitoring**: Tracking performance degradation over time

## Understanding RAG Evaluation

### Types of RAG Evaluation

RAG evaluation can be categorized into two main areas:

#### 1. Retrieval Evaluation
Measures how well the system finds relevant documents for a given query.

**Key Questions:**
- Does the system retrieve the most relevant documents?
- How well does the ranking match human judgment?
- What percentage of relevant documents are captured?

#### 2. Generation Evaluation
Measures the quality of generated responses using retrieved context.

**Key Questions:**
- Is the response factually accurate based on the context?
- How relevant is the response to the original query?
- Does the response contain harmful or inappropriate content?

### Evaluation Approaches

#### Automated Evaluation
- **Pros**: Fast, scalable, consistent
- **Cons**: May miss nuances, requires careful metric selection
- **Best for**: Large-scale testing, continuous monitoring

#### Human Evaluation
- **Pros**: Captures nuances, highly accurate
- **Cons**: Expensive, time-consuming, subjective
- **Best for**: Gold standard validation, edge case analysis

#### Hybrid Evaluation
- **Combines both approaches**: Automated for scale, human for validation
- **Best practice**: Use automated metrics for development, human evaluation for final validation

## Evaluation Metrics Explained

> **📍 Source Code Reference**: See `evaluate_retrieval_performance()` and `evaluate_generation_quality()` methods in `RAGEvaluationFramework`

### LlamaIndex Metrics

Our `RAGEvaluationFramework` implements LlamaIndex metrics through the `RetrieverEvaluator` and specialized evaluators.

#### Retrieval Metrics

> **🔧 Implementation**: `evaluate_retrieval_performance()` method uses `RetrieverEvaluator.from_metric_names()`

##### Mean Reciprocal Rank (MRR)
```python
# MRR calculation example (as implemented in our RetrieverEvaluator)
# If relevant document is at position 1: 1/1 = 1.0
# If relevant document is at position 2: 1/2 = 0.5
# If relevant document is at position 3: 1/3 = 0.33

# In our code:
retriever_evaluator = RetrieverEvaluator.from_metric_names(
    ["mrr", "hit_rate"], retriever=self.retriever
)
```

**What it measures**: Average reciprocal rank of the first relevant document  
**Range**: 0 to 1 (higher is better)  
**Use case**: When you care about finding the most relevant document quickly  
**Configuration**: Set `similarity_top_k` in `EvaluationConfig` to control retrieval count

##### Hit Rate
```python
# Hit Rate calculation example (as implemented in our RetrieverEvaluator)
# If any relevant document is in top-k results: 1
# If no relevant document is in top-k results: 0

# Access results in our framework:
results['retrieval_metrics']['hit_rate']  # From comprehensive_evaluation()
```

**What it measures**: Percentage of queries where at least one relevant document is retrieved  
**Range**: 0 to 1 (higher is better)  
**Use case**: When you want to ensure relevant information is available  
**Configuration**: Affected by `similarity_top_k` setting in `EvaluationConfig`

#### Generation Metrics

> **🔧 Implementation**: `evaluate_generation_quality()` method uses `FaithfulnessEvaluator` and `RelevancyEvaluator`

##### Faithfulness
```python
# Implementation in our framework:
faithfulness_evaluator = FaithfulnessEvaluator(
    service_context=self.evaluation_service_context
)
eval_result = faithfulness_evaluator.evaluate_response(response=response)
```

**What it measures**: Whether the response is grounded in the retrieved context  
**How it works**: Compares generated response against source documents  
**Range**: Boolean (True/False) or 0 to 1  
**Use case**: Preventing hallucinations and ensuring factual accuracy  
**Configuration**: Uses `evaluation_llm_model` from `EvaluationConfig` for more accurate evaluation

##### Relevancy
```python
# Implementation in our framework:
relevancy_evaluator = RelevancyEvaluator(
    service_context=self.evaluation_service_context
)
eval_result = relevancy_evaluator.evaluate_response(
    query=query, response=response
)
```

**What it measures**: How well the response addresses the original query  
**How it works**: Evaluates semantic similarity between query and response  
**Range**: Boolean (True/False) or 0 to 1  
**Use case**: Ensuring responses actually answer the question asked  
**Configuration**: Uses `evaluation_llm_model` for consistent evaluation

### RAGAS Metrics

> **🔧 Implementation**: `evaluate_with_ragas()` method integrates RAGAS framework  
> **⚙️ Configuration**: Set `enable_ragas=True` and configure `ragas_metrics` list in `EvaluationConfig`

```python
# RAGAS integration in our framework:
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.llama_index import evaluate as ragas_evaluate

# Usage in evaluate_with_ragas():
result = ragas_evaluate(self.query_engine, metrics, queries, ground_truths)
```

#### Faithfulness
```python
# RAGAS faithfulness is more nuanced than LlamaIndex
# It checks for factual consistency at a granular level
faithfulness_score = (number_of_correct_statements) / (total_number_of_statements)

# In our implementation:
if 'faithfulness' in self.config.ragas_metrics:
    metrics.append(faithfulness)
```

**Range**: 0 to 1 (higher is better)  
**Advantage**: More detailed analysis of factual accuracy  
**Configuration**: Included by default in `ragas_metrics` list

#### Answer Relevancy
```python
# Access in results:
ragas_results['ragas_answer_relevancy']  # From evaluate_with_ragas()
```

**What it measures**: Relevance of the generated answer to the question  
**How it works**: Uses semantic similarity and question-answer alignment  
**Range**: 0 to 1 (higher is better)  
**Advantage**: More sophisticated than simple relevancy checks  
**Configuration**: Enabled via `ragas_metrics` configuration

#### Context Precision
```python
# Measures precision of retrieved context
context_precision = (relevant_chunks_in_retrieved) / (total_retrieved_chunks)

# Configuration affects this metric:
similarity_top_k = config.similarity_top_k  # Controls retrieved chunks count
```

**What it measures**: Proportion of relevant chunks in retrieved context  
**Range**: 0 to 1 (higher is better)  
**Use case**: Optimizing retrieval to reduce noise  
**Configuration**: Affected by `similarity_top_k` and chunking parameters

#### Context Recall
```python
# Measures recall of retrieved context
context_recall = (relevant_chunks_retrieved) / (total_relevant_chunks_available)

# Influenced by our chunking strategy:
chunk_size = config.chunk_size     # From EvaluationConfig
chunk_overlap = config.chunk_overlap
```

**What it measures**: Proportion of relevant chunks successfully retrieved  
**Range**: 0 to 1 (higher is better)  
**Use case**: Ensuring no important information is missed  
**Configuration**: Optimized through chunk size and overlap settings

#### Harmfulness
```python
# Safety evaluation in our framework:
from ragas.metrics.critique import harmfulness

# Results access:
safety_score = ragas_results['ragas_harmfulness']  # Lower is better
```

**What it measures**: Whether the response contains harmful content  
**Range**: 0 to 1 (lower is better)  
**Use case**: Safety filtering and content moderation  
**Configuration**: Enable via `'harmfulness'` in `ragas_metrics` list

## Environment Setup

> **📁 Source Code**: Our implementation handles all imports and dependencies in `rag_metrics_evaluation_module.py`

### Prerequisites

1. **Python Environment**
```bash
python >= 3.8  # Required for our async implementations
```

2. **Required Packages** (as imported in our module)
```bash
# Core packages (imported in our implementation)
pip install llama-index==0.9.14.post3  # For LlamaIndex evaluators
pip install deeplake==3.8.12            # For vector storage
pip install openai==1.3.8               # For LLM and embeddings
pip install cohere==4.37                # For reranking (optional)
pip install ragas==0.0.22               # For RAGAS metrics
pip install pandas                       # For results processing
pip install html2text==2020.1.16        # For web content processing
```

> **💡 Tip**: Check the imports section at the top of `rag_metrics_evaluation_module.py` for the complete dependency list

3. **API Keys** (Required by our `RAGEvaluationFramework`)
Set up the following environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key"      # Required for LLM operations
export ACTIVELOOP_TOKEN="your_activeloop_token"  # For DeepLake vector store
export COHERE_API_KEY="your_cohere_api_key"      # Optional, for reranking
export LANGCHAIN_API_KEY="your_langsmith_key"    # Optional, for monitoring
```

### Configuration File Setup

Create a `.env` file in your project root (automatically loaded by our framework):
```env
OPENAI_API_KEY=your_openai_api_key_here
ACTIVELOOP_TOKEN=your_activeloop_token_here
COHERE_API_KEY=your_cohere_api_key_here
LANGCHAIN_API_KEY=your_langsmith_key_here
```

### Verify Installation

Test that everything works with our implementation:
```python
# Quick verification script
from src.rag_metrics_evaluation_module import RAGEvaluationFramework, EvaluationConfig

# This will validate all dependencies and API keys
try:
    config = EvaluationConfig()
    evaluator = RAGEvaluationFramework(config)
    print("✅ Environment setup successful!")
    print(f"🤖 LLM Model: {config.llm_model}")
    print(f"📊 RAGAS Available: {config.enable_ragas}")
except Exception as e:
    print(f"❌ Setup issue: {e}")
```

## Step-by-Step Implementation

### Step 1: Basic Setup

```python
from src.rag_metrics_evaluation_module import RAGEvaluationFramework, EvaluationConfig

# Configure evaluation settings
config = EvaluationConfig(
    llm_model="gpt-3.5-turbo",           # Main LLM for generation
    evaluation_llm_model="gpt-4",        # LLM for evaluation (more accurate)
    chunk_size=512,                      # Document chunk size
    chunk_overlap=32,                    # Overlap between chunks
    similarity_top_k=2,                  # Number of documents to retrieve
    enable_ragas=True,                   # Enable RAGAS metrics
    vector_store_type="simple"           # Vector store type
)

# Initialize evaluation framework
evaluator = RAGEvaluationFramework(config)
```

### Step 2: Document Setup

#### Option A: From Directory
```python
# Load documents from directory
documents_path = "path/to/your/documents"
vector_index = evaluator.setup_vector_store(documents_path=documents_path)
```

#### Option B: From Web Content
```python
from llama_index.readers.web import SimpleWebPageReader

# Load from web
documents = SimpleWebPageReader(html_to_text=True).load_data([
    "https://en.wikipedia.org/wiki/Artificial_intelligence"
])
vector_index = evaluator.setup_vector_store(documents=documents)
```

#### Option C: From Custom Documents
```python
from llama_index.core import Document

# Create custom documents
documents = [
    Document(text="Your document content here..."),
    Document(text="Another document content...")
]
vector_index = evaluator.setup_vector_store(documents=documents)
```

### Step 3: Generate Evaluation Dataset

```python
# Generate evaluation queries and dataset
dataset = evaluator.generate_evaluation_dataset(
    documents_path=documents_path  # or documents=documents
)

print(f"Generated {len(dataset['queries'])} evaluation queries")
print("Sample queries:", dataset['queries'][:3])
```

### Step 4: Run Retrieval Evaluation

```python
import asyncio

# Evaluate retrieval performance
retrieval_results = asyncio.run(
    evaluator.evaluate_retrieval_performance(dataset)
)

print("Retrieval Results:")
print(f"MRR: {retrieval_results['mrr']:.3f}")
print(f"Hit Rate: {retrieval_results['hit_rate']:.3f}")
```

### Step 5: Run Generation Evaluation

```python
# Evaluate generation quality
generation_results = asyncio.run(
    evaluator.evaluate_generation_quality(
        queries=dataset['queries'][:10]  # Limit for demo
    )
)

print("Generation Results:")
print(f"Faithfulness: {generation_results['faithfulness']:.3f}")
print(f"Relevancy: {generation_results['relevancy']:.3f}")
```

### Step 6: RAGAS Evaluation (Optional)

```python
# Prepare ground truth answers (you need to provide these)
ground_truths = [
    ["Expected answer 1"],
    ["Expected answer 2"],
    # ... more ground truth answers
]

# Run RAGAS evaluation
ragas_results = evaluator.evaluate_with_ragas(
    queries=dataset['queries'][:len(ground_truths)],
    ground_truths=ground_truths
)

print("RAGAS Results:")
for metric, score in ragas_results.items():
    print(f"{metric}: {score:.3f}")
```

### Step 7: Comprehensive Evaluation

```python
# Run all evaluations at once
comprehensive_results = asyncio.run(
    evaluator.comprehensive_evaluation(
        documents_path=documents_path,
        ground_truths=ground_truths  # Optional
    )
)

print("Comprehensive Evaluation Results:")
print("=================================")
print("Retrieval Metrics:", comprehensive_results['retrieval_metrics'])
print("Generation Metrics:", comprehensive_results['generation_metrics'])
print("RAGAS Metrics:", comprehensive_results['ragas_metrics'])
```

## Advanced Evaluation Techniques

### Batch Evaluation for Large Datasets

```python
# Configure for large-scale evaluation
config = EvaluationConfig(
    batch_size=20,      # Larger batch size
    workers=8,          # More parallel workers
    num_questions_per_chunk=3  # More questions per chunk
)

evaluator = RAGEvaluationFramework(config)

# Run evaluation on large dataset
results = asyncio.run(
    evaluator.comprehensive_evaluation(documents_path="large_document_collection")
)
```

### LLM Model Comparison

```python
# Compare different LLM models
models_to_compare = ["gpt-3.5-turbo", "gpt-4", "claude-3-sonnet"]

comparison_results = evaluator.compare_llm_performance(
    queries=dataset['queries'][:5],
    llm_models=models_to_compare
)

print("LLM Comparison Results:")
for model, results in comparison_results.items():
    print(f"{model}: {results}")
```

### Custom Evaluation Dataset

```python
# Create custom evaluation queries
custom_queries = [
    "What are the main benefits of artificial intelligence?",
    "How does machine learning differ from traditional programming?",
    "What are the ethical concerns around AI development?"
]

custom_ground_truths = [
    ["AI benefits include automation, improved decision-making, and efficiency gains"],
    ["ML learns from data patterns while traditional programming uses explicit rules"],
    ["Ethical concerns include bias, privacy, job displacement, and accountability"]
]

# Run evaluation with custom dataset
results = evaluator.evaluate_with_ragas(custom_queries, custom_ground_truths)
```

### Vector Store Comparison

```python
# Compare different vector store configurations
configs = [
    EvaluationConfig(vector_store_type="simple", chunk_size=256),
    EvaluationConfig(vector_store_type="simple", chunk_size=512),
    EvaluationConfig(vector_store_type="simple", chunk_size=1024)
]

for i, config in enumerate(configs):
    evaluator = RAGEvaluationFramework(config)
    results = asyncio.run(evaluator.comprehensive_evaluation(documents_path=documents_path))
    print(f"Config {i+1} (chunk_size={config.chunk_size}): {results['retrieval_metrics']}")
```

## Best Practices

### 1. Evaluation Strategy

#### Development Phase
- **Focus on**: Rapid iteration, quick feedback
- **Metrics**: Basic faithfulness and relevancy
- **Dataset size**: Small (10-50 queries)
- **Frequency**: Every major change

#### Pre-Production
- **Focus on**: Comprehensive assessment
- **Metrics**: All available metrics (LlamaIndex + RAGAS)
- **Dataset size**: Medium (100-500 queries)
- **Frequency**: Before each release

#### Production Monitoring
- **Focus on**: Performance tracking, degradation detection
- **Metrics**: Key performance indicators (KPIs)
- **Dataset size**: Large (1000+ queries)
- **Frequency**: Continuous monitoring

### 2. Metric Selection Guidelines

#### Choose Metrics Based on Use Case

**Information Retrieval Systems**
- Primary: MRR, Hit Rate, Context Precision
- Secondary: Answer Relevancy

**Question Answering Systems**
- Primary: Faithfulness, Answer Relevancy
- Secondary: Context Recall

**Safety-Critical Applications**
- Primary: Harmfulness, Faithfulness
- Secondary: All other metrics

### 3. Dataset Quality

#### Good Evaluation Datasets Have:
- **Diversity**: Cover various query types and difficulty levels
- **Representativeness**: Match real-world usage patterns
- **Quality**: Clear, unambiguous queries and answers
- **Size**: Sufficient for statistical significance

#### Creating Quality Datasets:
```python
# Automated dataset generation
dataset = evaluator.generate_evaluation_dataset(documents_path=documents_path)

# Manual curation (recommended for high-stakes applications)
curated_queries = [
    "Clear, specific question 1",
    "Complex multi-part question 2",
    "Edge case question 3"
]

# Validation dataset (separate from development dataset)
validation_queries = [
    "Validation question 1",
    "Validation question 2"
]
```

### 4. Performance Optimization

#### Evaluation Performance Tips:
- **Use batch evaluation** for large datasets
- **Limit query count** during development
- **Cache evaluation results** to avoid re-computation
- **Use parallel workers** for faster processing

```python
# Optimized evaluation configuration
config = EvaluationConfig(
    workers=8,              # Parallel processing
    batch_size=20,          # Larger batches
    chunk_size=512,         # Optimal chunk size
    similarity_top_k=3      # Balanced retrieval
)
```

### 5. Interpreting Results

#### Score Interpretation Guidelines:

**Retrieval Metrics**
- MRR > 0.7: Excellent retrieval performance
- MRR 0.4-0.7: Good retrieval performance
- MRR < 0.4: Needs improvement

**Generation Metrics**
- Faithfulness > 0.8: High factual accuracy
- Relevancy > 0.8: Good query-response alignment
- Harmfulness < 0.1: Safe content generation

#### Red Flags:
- **Sudden performance drops**: Possible system degradation
- **High variance**: Inconsistent performance across queries
- **Perfect scores**: Possible evaluation errors or overfitting

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Import Errors
```bash
ImportError: No module named 'ragas'
```
**Solution:**
```bash
pip install ragas==0.0.22
```

#### Issue 2: API Key Errors
```bash
openai.error.AuthenticationError: Incorrect API key provided
```
**Solution:**
```python
import os
os.environ["OPENAI_API_KEY"] = "your_actual_api_key"
```

#### Issue 3: Memory Issues with Large Documents
```bash
RuntimeError: CUDA out of memory
```
**Solution:**
```python
config = EvaluationConfig(
    chunk_size=256,        # Smaller chunks
    batch_size=5,          # Smaller batches
    similarity_top_k=2     # Fewer retrieved documents
)
```

#### Issue 4: Slow Evaluation Performance
**Solutions:**
```python
# Increase parallel workers
config = EvaluationConfig(workers=8)

# Use faster LLM for evaluation
config = EvaluationConfig(evaluation_llm_model="gpt-3.5-turbo")

# Limit evaluation dataset size
results = evaluator.evaluate_generation_quality(queries[:10])
```

#### Issue 5: Inconsistent Results
**Potential Causes:**
- Non-deterministic LLM responses (temperature > 0)
- Random document chunking
- Evaluation dataset quality

**Solutions:**
```python
# Use deterministic settings
config = EvaluationConfig(
    llm_temperature=0.0,
    evaluation_llm_model="gpt-4"  # More consistent
)

# Use fixed random seeds
import random
random.seed(42)
```

## Practical Examples

### Example 1: Basic Document QA System

```python
# Setup for document QA evaluation
config = EvaluationConfig(
    llm_model="gpt-3.5-turbo",
    chunk_size=512,
    similarity_top_k=3,
    enable_ragas=True
)

evaluator = RAGEvaluationFramework(config)

# Load documents
documents_path = "knowledge_base/"
vector_index = evaluator.setup_vector_store(documents_path=documents_path)

# Generate evaluation dataset
dataset = evaluator.generate_evaluation_dataset(documents_path=documents_path)

# Run comprehensive evaluation
results = asyncio.run(evaluator.comprehensive_evaluation(documents_path=documents_path))

print("Document QA Evaluation Results:")
print(f"Retrieval MRR: {results['retrieval_metrics']['mrr']:.3f}")
print(f"Generation Faithfulness: {results['generation_metrics']['faithfulness']:.3f}")
```

### Example 2: Multi-Model Comparison

```python
# Compare different models for the same task
models = ["gpt-3.5-turbo", "gpt-4"]
results_comparison = {}

for model in models:
    config = EvaluationConfig(llm_model=model)
    evaluator = RAGEvaluationFramework(config)
    
    # Setup with same documents
    evaluator.setup_vector_store(documents_path=documents_path)
    
    # Evaluate
    results = asyncio.run(evaluator.evaluate_generation_quality(dataset['queries'][:5]))
    results_comparison[model] = results

print("Model Comparison:")
for model, metrics in results_comparison.items():
    print(f"{model}: Faithfulness={metrics['faithfulness']:.3f}, Relevancy={metrics['relevancy']:.3f}")
```

### Example 3: Production Monitoring Setup

```python
# Production monitoring configuration
production_config = EvaluationConfig(
    llm_model="gpt-4",
    evaluation_llm_model="gpt-4",
    chunk_size=512,
    workers=4,
    enable_ragas=False  # Faster evaluation for monitoring
)

evaluator = RAGEvaluationFramework(production_config)

# Setup monitoring dataset (representative of production queries)
monitoring_queries = [
    "Production query type 1",
    "Production query type 2",
    # ... more representative queries
]

# Regular monitoring evaluation
def run_monitoring_evaluation():
    results = asyncio.run(
        evaluator.evaluate_generation_quality(monitoring_queries)
    )
    
    # Check for degradation
    if results['faithfulness'] < 0.8:
        print("WARNING: Faithfulness score below threshold!")
    
    if results['relevancy'] < 0.8:
        print("WARNING: Relevancy score below threshold!")
    
    return results

# Run monitoring (schedule this regularly in production)
monitoring_results = run_monitoring_evaluation()
```

### Example 4: A/B Testing RAG Configurations

```python
# A/B test different chunk sizes
configurations = [
    {"name": "Small Chunks", "chunk_size": 256, "similarity_top_k": 5},
    {"name": "Medium Chunks", "chunk_size": 512, "similarity_top_k": 3},
    {"name": "Large Chunks", "chunk_size": 1024, "similarity_top_k": 2}
]

ab_test_results = {}

for config_info in configurations:
    config = EvaluationConfig(
        chunk_size=config_info["chunk_size"],
        similarity_top_k=config_info["similarity_top_k"]
    )
    
    evaluator = RAGEvaluationFramework(config)
    evaluator.setup_vector_store(documents_path=documents_path)
    
    # Run evaluation
    results = asyncio.run(evaluator.comprehensive_evaluation(documents_path=documents_path))
    ab_test_results[config_info["name"]] = results

# Compare results
print("A/B Test Results:")
for config_name, results in ab_test_results.items():
    retrieval_mrr = results['retrieval_metrics']['mrr']
    generation_faithfulness = results['generation_metrics']['faithfulness']
    print(f"{config_name}: MRR={retrieval_mrr:.3f}, Faithfulness={generation_faithfulness:.3f}")
```

## Exploring the Source Code

> **📁 File**: [`src/rag_metrics_evaluation_module.py`](../src/rag_metrics_evaluation_module.py)

Want to understand how everything works under the hood? Here's a guide to exploring our implementation:

### 🏗️ Code Structure

```python
# 1. Configuration Management (Lines ~50-80)
@dataclass
class EvaluationConfig:
    """All evaluation settings in one place"""
    
# 2. Main Framework Class (Lines ~90-600+)
class RAGEvaluationFramework:
    """The heart of our evaluation system"""
    
    def __init__(self, config: EvaluationConfig):
        """Initialization and LLM setup"""
        
    def setup_vector_store(self, ...):
        """Vector store and index creation"""
        
    def evaluate_retrieval_performance(self, ...):
        """MRR and Hit Rate evaluation"""
        
    def evaluate_generation_quality(self, ...):
        """Faithfulness and Relevancy evaluation"""
        
    def evaluate_with_ragas(self, ...):
        """RAGAS metrics integration"""
        
    def comprehensive_evaluation(self, ...):
        """All-in-one evaluation pipeline"""

# 3. Example Usage (Lines ~700+)
def example_usage():
    """Ready-to-run examples"""
```

### 🔍 Key Implementation Details

#### Async Evaluation Pattern
```python
# Look for this pattern in our code:
async def evaluate_retrieval_performance(self, qa_dataset):
    eval_results = await retriever_evaluator.aevaluate_dataset(qa_dataset['qa_dataset'])
    # Non-blocking evaluation for better performance
```

#### Error Handling Strategy
```python
# Our robust error handling pattern:
try:
    result = await query_engine.aquery(query)
    logger.info("Evaluation completed successfully")
except Exception as e:
    logger.error(f"Evaluation failed: {e}")
    raise
```

#### Configuration-Driven Design
```python
# Everything is configurable:
if self.config.enable_ragas and RAGAS_AVAILABLE:
    # RAGAS evaluation
if 'faithfulness' in self.config.ragas_metrics:
    # Specific metric evaluation
```

### 🛠️ Customization Points

Want to extend our implementation? Here are the main extension points:

1. **Add New Metrics**: Extend the `ragas_metrics` list or add custom evaluators
2. **New Vector Stores**: Add support in `setup_vector_store()` method
3. **Custom LLMs**: Extend LLM initialization in `_setup_llms()`
4. **Export Formats**: Add new formats in `export_results()` method

### 📖 Learning from the Code

#### Best Practices Demonstrated
- **Dataclass Configuration**: Clean, typed configuration management
- **Async Programming**: Non-blocking operations for scalability
- **Logging Integration**: Comprehensive logging for debugging
- **Exception Handling**: Graceful error handling throughout
- **Type Hints**: Full type annotation for better code clarity

#### Advanced Patterns
- **Service Context Management**: Separate contexts for generation vs evaluation
- **Batch Processing**: Efficient handling of large evaluation datasets
- **Results Aggregation**: Clean aggregation of metrics from multiple sources
- **Configuration Validation**: Runtime validation of configuration settings

## Conclusion

RAG evaluation is essential for building reliable, high-quality retrieval-augmented generation systems. This guide has covered:

- **Comprehensive evaluation metrics** from both LlamaIndex and RAGAS
- **Step-by-step implementation** using our `RAGEvaluationFramework`
- **Advanced techniques** for large-scale and production evaluation
- **Best practices** for creating quality evaluation datasets
- **Troubleshooting guidance** for common issues
- **Source code exploration** for deeper understanding

### Key Takeaways:

1. **Start simple**: Begin with basic faithfulness and relevancy metrics using our framework
2. **Iterate frequently**: Evaluate after each significant change with `comprehensive_evaluation()`
3. **Use multiple metrics**: Our implementation supports both LlamaIndex and RAGAS metrics
4. **Validate with humans**: Automated metrics are good, but human validation is gold standard
5. **Monitor in production**: Use our batch evaluation for continuous monitoring

### Next Steps:

1. **Implement basic evaluation** using `RAGEvaluationFramework` for your RAG system
2. **Create a representative evaluation dataset** with our `generate_evaluation_dataset()` method
3. **Set up monitoring** using our production monitoring patterns
4. **Experiment with different configurations** using `EvaluationConfig` options
5. **Establish evaluation workflows** with our `comprehensive_evaluation()` method

### 🚀 Get Started Now:

```python
# Your RAG evaluation journey starts here:
from src.rag_metrics_evaluation_module import RAGEvaluationFramework, EvaluationConfig

config = EvaluationConfig()  # Start with defaults
evaluator = RAGEvaluationFramework(config)

# Point to your documents and run evaluation
results = asyncio.run(
    evaluator.comprehensive_evaluation(documents_path="your/docs/path")
)

print(f"🎯 Your RAG system quality score: {results}")
```

Remember: The goal of evaluation is not to achieve perfect scores, but to understand your system's performance and make informed improvements. Our `RAGEvaluationFramework` makes this process systematic, scalable, and actionable. Regular evaluation is the key to building robust RAG applications that deliver reliable, high-quality results.

---

## Quick Reference

### 📚 Class & Method Reference

#### `EvaluationConfig` (Configuration)
```python
config = EvaluationConfig(
    llm_model="gpt-3.5-turbo",        # Generation LLM
    evaluation_llm_model="gpt-4",      # Evaluation LLM (more accurate)
    chunk_size=512,                    # Document chunking size
    similarity_top_k=3,                # Retrieval count
    enable_ragas=True,                 # Enable RAGAS metrics
    workers=8,                         # Parallel processing
    batch_size=20                      # Batch evaluation size
)
```

#### `RAGEvaluationFramework` (Main Class)
```python
# Initialize
evaluator = RAGEvaluationFramework(config)

# Setup vector store
evaluator.setup_vector_store(documents_path="docs/")

# Generate evaluation dataset
dataset = evaluator.generate_evaluation_dataset(documents_path="docs/")

# Individual evaluations
retrieval_results = await evaluator.evaluate_retrieval_performance(dataset)
generation_results = await evaluator.evaluate_generation_quality(dataset['queries'])
ragas_results = evaluator.evaluate_with_ragas(queries, ground_truths)

# All-in-one evaluation
results = await evaluator.comprehensive_evaluation(documents_path="docs/")

# Compare models
comparison = evaluator.compare_llm_performance(queries, ["gpt-3.5-turbo", "gpt-4"])

# Export results
df = evaluator.export_results("pandas")
```

### 🎯 Common Workflows

#### Quick Evaluation
```python
from src.rag_metrics_evaluation_module import RAGEvaluationFramework, EvaluationConfig
import asyncio

evaluator = RAGEvaluationFramework(EvaluationConfig())
results = asyncio.run(evaluator.comprehensive_evaluation(documents_path="docs/"))
```

#### Production Monitoring
```python
config = EvaluationConfig(enable_ragas=False, workers=4)  # Faster evaluation
evaluator = RAGEvaluationFramework(config)
results = asyncio.run(evaluator.evaluate_generation_quality(monitoring_queries))
```

#### A/B Testing
```python
models = ["gpt-3.5-turbo", "gpt-4"]
comparison = evaluator.compare_llm_performance(test_queries, models)
```

### 📊 Results Structure
```python
results = {
    'retrieval_metrics': {'mrr': 0.85, 'hit_rate': 0.92},
    'generation_metrics': {'faithfulness': 0.88, 'relevancy': 0.91},
    'ragas_metrics': {'ragas_faithfulness': 0.87, 'ragas_answer_relevancy': 0.89},
    'evaluation_config': {...}
}
```