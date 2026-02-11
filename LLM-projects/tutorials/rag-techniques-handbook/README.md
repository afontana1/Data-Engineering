# RAG Techniques Handbook

> **🎯 Status**: Production-Ready | **📚 Complete Techniques**: 6 | **🔗 Integrated Docs**: 100%

## Overview

This repository provides a comprehensive collection of **advanced RAG (Retrieval Augmented Generation) techniques** with production-ready implementations and seamlessly integrated documentation. Each technique includes both theoretical explanations and working Python code that you can immediately use in your projects.

**Key Features:**
- ✅ **Production-Ready Code**: All implementations are tested and optimized
- 📖 **Integrated Documentation**: Theory and code seamlessly connected
- 🚀 **Quick Start Guides**: Get running in 3 minutes with any technique
- 🔧 **Configurable**: Extensive configuration options for customization
- 📊 **Evaluation Framework**: Built-in metrics and performance assessment
- 🤖 **Multiple LLM Support**: OpenAI, Cohere, and more

## Currently Implemented Techniques

### ✅ RAG Metrics & Evaluation
**Complete evaluation framework with LlamaIndex and RAGAS integration**
- **Features**: Retrieval metrics (MRR, Hit Rate), Generation quality (Faithfulness, Relevancy), RAGAS comprehensive metrics
- **Classes**: `RAGEvaluationFramework`, `EvaluationConfig`
- **Documentation**: [RAG Metrics & Evaluation Guide](docs/rag_metrics_evaluation_guide.md)
- **Implementation**: [rag_metrics_evaluation_module.py](src/rag_metrics_evaluation_module.py)

### ✅ Vector Store Index Implementation
**Optimized vector store operations with DeepLake integration**
- **Features**: Deep Memory optimization, Performance evaluation, Cohere reranking, Async operations
- **Classes**: `VectorStoreManager`, `VectorStoreConfig`
- **Documentation**: [Vector Store Implementation Guide](docs/vector_store_index_implementation_guide.md)
- **Implementation**: [vector_store_index_implementation.py](src/vector_store_index_implementation.py)

### ✅ Advanced Reranking Systems
**Multiple reranking strategies with ensemble capabilities**
- **Features**: Cohere API, SentenceTransformer, LLM-based, Ensemble reranking, Performance caching
- **Classes**: `RerankerManager`, `RerankerConfig`, `EnsembleReranker`
- **Documentation**: [Reranking Systems Guide](docs/reranking_rag_systems.md)
- **Implementation**: [reranking_rag_systems.py](src/reranking_rag_systems.py)

### ✅ Advanced RAG Techniques
**LlamaIndex-based advanced query processing and retrieval**
- **Features**: Sub-question decomposition, Query transformation, Hierarchical retrieval, Streaming support
- **Classes**: `AdvancedRAGEngine`
- **Documentation**: [Advanced RAG Techniques Guide](docs/Advanced_RAg_techniques_LLamaIndex.md)
- **Implementation**: [Advanced_RAG_tenchniques_LLamaIndex.py](src/Advanced_RAG_tenchniques_LLamaIndex.py)

### ✅ RAG Agent System
**Multi-source agent-based RAG with tool integration**
- **Features**: Multi-document querying, Tool integration, OpenAI agents, DeepLake support
- **Classes**: `RAGAgent`
- **Documentation**: [RAG Agent Guide](docs/LlamaIndex_rag_agent.md)
- **Implementation**: [LlamaIndex_rag_agent.py](src/LlamaIndex_rag_agent.py)

### ✅ LangSmith Integration
**Complete monitoring and evaluation with LangSmith**
- **Features**: Tracing, Prompt management, Evaluation pipelines, Chain monitoring
- **Classes**: `LangSmithManager`
- **Documentation**: [LangSmith Integration Guide](docs/Langsmith.md)
- **Implementation**: [Langsmith.py](src/Langsmith.py)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/sosanzma/rag-techniques-handbook.git
cd rag-techniques-handbook

# Install dependencies
pip install llama-index==0.9.14.post3 deeplake==3.8.12 openai==1.3.8 cohere==4.37 ragas==0.0.22 pandas

# Set up environment variables
export OPENAI_API_KEY="your_openai_key"
export ACTIVELOOP_TOKEN="your_deeplake_token"
export COHERE_API_KEY="your_cohere_key"
```

### 3-Minute Example: Complete RAG Evaluation

```python
from src.rag_metrics_evaluation_module import RAGEvaluationFramework, EvaluationConfig
import asyncio

# Configure and run comprehensive evaluation
config = EvaluationConfig(llm_model="gpt-3.5-turbo", enable_ragas=True)
evaluator = RAGEvaluationFramework(config)

# Evaluate your documents
results = asyncio.run(
    evaluator.comprehensive_evaluation(documents_path="your/docs/path")
)

print(f"📊 Retrieval MRR: {results['retrieval_metrics']['mrr']:.3f}")
print(f"✅ Faithfulness: {results['generation_metrics']['faithfulness']:.3f}")
print(f"🎯 Relevancy: {results['generation_metrics']['relevancy']:.3f}")
```

## Project Structure

```
rag-techniques-handbook/
├── 📁 docs/                           # Comprehensive guides (theory + implementation)
│   ├── 📋 rag_metrics_evaluation_guide.md
│   ├── 📋 vector_store_index_implementation_guide.md
│   ├── 📋 reranking_rag_systems.md
│   ├── 📋 Advanced_RAg_techniques_LLamaIndex.md
│   ├── 📋 LlamaIndex_rag_agent.md
│   └── 📋 Langsmith.md
├── 🐍 src/                            # Production-ready implementations
│   ├── 🔬 rag_metrics_evaluation_module.py
│   ├── 🗄️ vector_store_index_implementation.py
│   ├── 🔄 reranking_rag_systems.py
│   ├── 🚀 Advanced_RAG_tenchniques_LLamaIndex.py
│   ├── 🤖 LlamaIndex_rag_agent.py
│   └── 📈 Langsmith.py
├── 📓 src/Module_04_RAG_Metrics&Evaluation.ipynb  # Jupyter notebook example
├── 📖 CLAUDE.md                       # Development documentation
└── 🗺️ README.md                       # This file
```



## Prerequisites

- **Python**: 3.8+
- **API Keys**: OpenAI (required), Cohere (optional), ActiveLoop (for DeepLake)
- **Memory**: 8GB+ RAM recommended for large document processing
- **Storage**: Vector databases may require significant disk space

## Contributing

We welcome contributions! The repository is designed for easy extension:

### Current Areas for Contribution
- Additional evaluation metrics
- New vector store integrations
- Performance optimizations
- Documentation improvements
- Example notebooks

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Follow the existing patterns (see any `src/` file for reference)
4. Update both implementation and documentation
5. Submit a pull request

## Resources

### Documentation
- **[CLAUDE.md](CLAUDE.md)**: Complete technical documentation and development guide
- **[Planned Features](PLANNED_FEATURES.md)**: Upcoming techniques and improvements

### External Resources
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [RAGAS Documentation](https://docs.ragas.io/)
- [DeepLake Documentation](https://docs.deeplake.ai/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

> **🚀 Ready to get started?** Pick any technique from the list above and follow its Quick Start guide. Each implementation is production-ready and includes comprehensive documentation to get you running in minutes!
