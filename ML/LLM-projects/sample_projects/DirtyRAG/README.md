# DirtyRAG

A smol [RAG](https://www.databricks.com/glossary/retrieval-augmented-generation-rag)-based framework for working with large language models [(LLMs)](https://en.wikipedia.org/wiki/Large_language_model).

## Motivation

As LLM-based applications scale, especially ones that leverage RAG-based architectures, having more granular control is important. This control should be able to support complex conditional reasoning, hybrid search, agents and more.

## Goals

The goal is to have a minimal LLM RAG framework with support for common RAG-based workflows.

First-class support for popular vector databases to pull embeddings for semantic search (FAISS, ChromaDB, Postgres w/ pgvector) will be imperative to improve relevancy.

Additionally, this tool will have support for building custom agents and tools that can combine with large language models to build complex analysis tools (i.e hybrid search). This will involve defining how iterations are done, chains and conditional reasoning workflows.

# Examples

_Simple RAG based product recommendation tool that leverages a hybrid search approach to reason about it's results_

```txt
🧠 Searching Best noise cancelling headphones
----------------------------------------------

Cleansing data...
Parsing content...
Thinking...

----------------------------------------------
RESULTS:
----------------------------------------------

Product: QuietComfort 35 II Noise Cancelling Wireless Headphones
Link: https://global.bose.com/content/consumer_electronics/b2c_catalog/worldwide/websites/en_ae/product/qc35_ii.html

Product: Sony WH1000XM4/B Premium Noise Cancelling Wireless ...
Link: https://electronics.sony.com/audio/headphones/headband/p/wh1000xm4-b

Product: SENNHEISER Momentum 3 Wireless Noise Cancelling ...
Link: https://www.amazon.com/Sennheiser-Momentum-Cancelling-Headphones-Functionality/dp/B07VW98ZKG
```
