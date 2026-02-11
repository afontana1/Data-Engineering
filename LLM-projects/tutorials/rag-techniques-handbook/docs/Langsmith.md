# Understanding LangSmith: A Guide to LLM Development & Evaluation

**📁 Implementation File**: [`src/Langsmith.py`](../src/Langsmith.py)

This guide covers LangSmith concepts and their practical implementation through the `LangSmithManager` class. Follow along with the production-ready Python code for hands-on experience.

## 🚀 Quick Start (3 Minutes)

Get up and running with LangSmith monitoring using our `LangSmithManager` implementation:

```python
from src.Langsmith import LangSmithManager
from langchain_core.prompts import ChatPromptTemplate

# 1. Initialize LangSmith Manager
manager = LangSmithManager(
    api_key="your-langsmith-api-key",
    project_name="my-first-project"
)

# 2. Create a monitored prompt template
prompt = manager.create_prompt_template(
    template="Explain {topic} in simple terms for a beginner.",
    handle="beginner-explainer-v1"
)

# 3. Create and run a monitored chain
chain = manager.create_monitored_chain(prompt)
response = chain.invoke({"topic": "machine learning"})

print(f"Response: {response}")
# Check LangSmith dashboard for trace details!
```

**Prerequisites**: Set your OpenAI API key: `export OPENAI_API_KEY="your-openai-key"`

**Next Steps**: Visit [LangSmith Dashboard](https://smith.langchain.com) to see your traces!

## What is LangSmith?
LangSmith is a developer platform designed to streamline the development, testing, and monitoring of Large Language Model (LLM) applications. Think of it as a specialized IDE (Integrated Development Environment) for LLM applications that helps you:
- Debug your LLM chains and agents
- Test different prompts and evaluate their effectiveness
- Monitor your application's performance in real-time
- Track and optimize costs related to LLM API usage

## 📋 Module Overview

Our `LangSmithManager` class (lines 22-148) provides a complete implementation for LangSmith integration:

### Core Class: `LangSmithManager`

**Constructor Parameters** (lines 27-32):
- `api_key`: Your LangSmith API key
- `project_name`: Project identifier for tracing
- `endpoint`: LangSmith API endpoint (defaults to official endpoint)

### Key Methods

#### Environment Setup
- **`setup_environment()`** (lines 45-51): Configures environment variables for LangSmith tracing

#### Prompt Management
- **`create_prompt_template()`** (lines 53-72): Creates and versions prompt templates in LangSmith Hub
- **`create_qa_chain()`** (lines 74-97): Builds QA chains with retrieval capabilities

#### Monitoring & Evaluation
- **`create_monitored_chain()`** (lines 128-147): Creates chains with automatic tracing
- **`evaluate_responses()`** (lines 99-126): Evaluates model outputs against references

### Usage Pattern
```python
# Initialize
manager = LangSmithManager(api_key="...", project_name="...")

# Create prompt → Build chain → Run with monitoring → Evaluate
prompt = manager.create_prompt_template("...", "handle")
chain = manager.create_monitored_chain(prompt)
result = chain.invoke({...})
evaluation = manager.evaluate_responses([result], [reference])
```

## Why Do We Need LangSmith?

### The Challenge of LLM Development
When building LLM applications, developers face several challenges:
1. **Inconsistent Outputs**: LLMs can produce different responses to the same prompt
2. **Hard-to-Track Errors**: Debugging complex chains of LLM interactions is difficult
3. **Cost Management**: LLM API calls can be expensive and need optimization
4. **Quality Assurance**: Ensuring consistent, high-quality responses is challenging

### How LangSmith Solves These Problems
LangSmith provides solutions through three main functionalities:

#### 1. Development & Debugging
```python
# Using our LangSmithManager implementation
from src.Langsmith import LangSmithManager

# Initialize with automatic environment setup (see setup_environment method)
manager = LangSmithManager(
    api_key="your-api-key",
    project_name="debug_project"
)

# Create a monitored chain for debugging
prompt = manager.create_prompt_template(
    template="Explain why {question} in scientific terms.",
    handle="science-explainer-v1"
)

# Chain automatically traces each step
chain = manager.create_monitored_chain(prompt)
response = chain.invoke({"question": "the sky is blue"})

# View detailed traces in LangSmith dashboard
```

#### 2. Testing & Evaluation
```python
# Using our LangSmithManager's evaluate_responses method
test_questions = ["What is 2+2?", "What is the capital of France?"]
expected_answers = ["4", "Paris"]

# Generate predictions using our monitored chain
predictions = []
for question in test_questions:
    response = chain.invoke({"question": question})
    predictions.append(response)

# Evaluate using built-in evaluation method
results = manager.evaluate_responses(
    predictions=predictions,
    references=expected_answers,
    criteria="accuracy"  # Uses load_evaluator internally
)

print("Evaluation Results:", results)
```

#### 3. Monitoring & Optimization
- Track token usage and costs
- Monitor response times
- Identify performance bottlenecks

## Real-World Use Cases

### 1. Customer Service Chatbots
**Problem**: Ensuring consistent and accurate responses to customer queries.
**Solution with LangSmith**:
- Test different prompt variations
- Monitor response quality
- Track and optimize costs
- Debug complex conversation flows

### 2. Content Generation
**Problem**: Maintaining quality across different types of generated content.
**Solution with LangSmith**:
- Evaluate content quality automatically
- Test different generation strategies
- Monitor for inappropriate content
- Track generation performance

### 3. Research and Analysis
**Problem**: Ensuring accuracy in information extraction and analysis.
**Solution with LangSmith**:
- Validate extracted information
- Monitor source usage
- Track reasoning chains
- Evaluate conclusion accuracy

## Best Practices Guide

### 1. Prompt Development
```python
# Version control your prompts using LangSmithManager
# Uses create_prompt_template method (lines 53-72)

# Version 1
prompt_v1 = manager.create_prompt_template(
    template="Tell me about {topic}",
    handle="topic-explainer-v1",
    public=False  # Keep private during development
)

# Version 2 - more detailed
prompt_v2 = manager.create_prompt_template(
    template="Provide a detailed explanation of {topic} with examples",
    handle="topic-explainer-v2"
)

# Test both versions with same input
chain_v1 = manager.create_monitored_chain(prompt_v1)
chain_v2 = manager.create_monitored_chain(prompt_v2)

# Compare results in LangSmith dashboard
response_v1 = chain_v1.invoke({"topic": "quantum computing"})
response_v2 = chain_v2.invoke({"topic": "quantum computing"})
```

### 2. Testing Strategy
1. **Unit Testing**: Test individual components
   - Prompt responses
   - Chain steps
   - Tool usage

2. **Integration Testing**: Test complete flows
   - End-to-end conversations
   - Complex reasoning chains
   - Multi-tool interactions

3. **Quality Assurance**: Evaluate outputs
   - Factual accuracy
   - Response relevance
   - Output formatting

### 3. Monitoring Setup
```python
# Automatic monitoring setup with LangSmithManager
# Environment configuration handled by setup_environment method (lines 45-51)

manager = LangSmithManager(
    api_key="your-api-key",
    project_name="production-monitoring",
    endpoint="https://api.smith.langchain.com"  # Optional, uses default
)

# All chains created through manager are automatically monitored
chain = manager.create_monitored_chain(prompt)

# Metrics automatically tracked in LangSmith:
# - Response time
# - Token usage
# - Model information
# - Input/output pairs
# - Error traces
# - Cost tracking

response = chain.invoke({"topic": "machine learning"})
# Check LangSmith dashboard for automatic metrics collection
```

## Common Challenges and Solutions

### 1. High Token Usage
**Problem**: Excessive costs from inefficient token usage
**Solution**: 
- Use LangSmith to track token usage patterns
- Implement caching for common queries
- Optimize prompt design

### 2. Inconsistent Quality
**Problem**: Varying response quality across different queries
**Solution**:
- Set up automated quality evaluations
- Use versioned prompts
- Implement feedback loops

### 3. Complex Debugging
**Problem**: Difficult to trace issues in complex chains
**Solution**:
- Enable detailed tracing
- Use structured logging
- Implement step-by-step validation

## Getting Started Tutorial

### Step 1: Setup
```python
# Install required packages
pip install langchain langsmith langchain-openai

# Set up environment variables
export OPENAI_API_KEY="your-openai-key"
export LANGCHAIN_API_KEY="your-langsmith-key"
```

### Step 2: Basic Implementation
```python
# Import our LangSmithManager implementation
from src.Langsmith import LangSmithManager

# Initialize LangSmith (automatically sets up environment)
manager = LangSmithManager(
    api_key="your-langsmith-key",
    project_name="getting-started-tutorial"
)

# Create your first versioned prompt
prompt = manager.create_prompt_template(
    template="Answer this question clearly: {question}",
    handle="basic-qa-v1"
)

# Create monitored chain
chain = manager.create_monitored_chain(prompt)
```

### Step 3: Run and Monitor
```python
# All monitoring is automatically enabled
response = chain.invoke({"question": "What is artificial intelligence?"})
print(f"Response: {response}")

# Optional: Evaluate the response
evaluation = manager.evaluate_responses(
    predictions=[response],
    references=["AI is the simulation of human intelligence..."],
    criteria="accuracy"
)
print(f"Evaluation: {evaluation}")
```

## Advanced Topics

### 1. QA Chain with Retrieval
Build sophisticated QA systems using the `create_qa_chain` method:
```python
from langchain_community.vectorstores import DeepLake

# Assume you have a vectorstore setup
vectorstore = DeepLake(dataset_path="path/to/your/dataset")

# Create QA chain with retrieval (see method lines 74-97)
qa_chain = manager.create_qa_chain(
    vectorstore=vectorstore,
    prompt_handle="qa-with-context-v1"  # Previously created prompt
)

# Run with automatic tracing
response = qa_chain({"query": "What are the key benefits of RAG?"})
```

### 2. Custom Evaluation Workflows
Extend the `evaluate_responses` method for domain-specific evaluation:
```python
# Evaluate multiple criteria
criteria_list = ["accuracy", "relevance", "completeness"]
evaluations = {}

for criteria in criteria_list:
    results = manager.evaluate_responses(
        predictions=[response],
        references=[reference_answer],
        criteria=criteria
    )
    evaluations[criteria] = results

print("Multi-criteria evaluation:", evaluations)
```

### 3. Production Monitoring Pattern
Combine all LangSmithManager methods for production use:
```python
# Production setup with error handling
def production_llm_pipeline(question: str, reference: str = None):
    try:
        # 1. Create/load prompt
        prompt = manager.create_prompt_template(
            template="Professional answer for: {question}",
            handle="production-qa-v1"
        )
        
        # 2. Run monitored chain
        chain = manager.create_monitored_chain(prompt)
        response = chain.invoke({"question": question})
        
        # 3. Optional evaluation
        if reference:
            evaluation = manager.evaluate_responses(
                predictions=[response],
                references=[reference]
            )
            return response, evaluation
        
        return response
        
    except Exception as e:
        print(f"Pipeline error: {e}")
        return None

# Usage
result = production_llm_pipeline("Explain quantum computing")
```

## 🔍 Source Code Exploration

Dive deeper into the implementation details:

### File Structure
- **Lines 1-21**: Imports and module documentation
- **Lines 22-148**: `LangSmithManager` class implementation
- **Lines 150-188**: Example usage in `main()` function

### Key Implementation Details

#### Environment Configuration (Lines 45-51)
```python
@staticmethod
def setup_environment(api_key: str, project_name: str, endpoint: str) -> None:
    """Automatically configures all required environment variables"""
```
This method handles the tedious setup of LangSmith environment variables that you'd otherwise need to set manually.

#### Prompt Template Management (Lines 53-72)
```python
def create_prompt_template(self, template: str, handle: str, public: bool = False):
    """Creates versioned prompts with LangChain Hub integration"""
```
- Uses `hub.push()` for version control
- Supports public/private prompts
- Returns `ChatPromptTemplate` for chain building

#### Chain Creation Patterns (Lines 128-147)
```python
def create_monitored_chain(self, prompt_template: ChatPromptTemplate):
    """Creates LCEL chains with automatic tracing"""
    chain = (
        prompt_template
        | self.llm
        | self.output_parser
    )
```
Uses LangChain Expression Language (LCEL) for clean, traceable chains.

#### Evaluation Integration (Lines 99-126)
```python
def evaluate_responses(self, predictions: List[str], references: List[str]):
    """Built-in evaluation using LangChain evaluators"""
```
- Leverages `load_evaluator()` from LangChain
- Supports multiple evaluation criteria
- Returns structured evaluation results

### Extending the Implementation

Want to add custom functionality? Key extension points:
1. **Custom Evaluators**: Extend the `evaluate_responses` method
2. **Different LLMs**: Modify the `__init__` method's `self.llm` initialization
3. **Advanced Chains**: Add methods similar to `create_qa_chain` for other chain types
4. **Custom Parsers**: Replace `StrOutputParser` with domain-specific parsers

## Conclusion
LangSmith is a powerful tool that makes LLM application development more manageable and reliable. By following this guide and implementing the suggested practices, you can:
- Develop more robust LLM applications
- Ensure consistent quality in responses
- Optimize costs and performance
- Debug complex issues effectively

## 📚 Quick Reference

### `LangSmithManager` Class Summary

| Method | Lines | Purpose | Key Parameters |
|--------|-------|---------|---------------|
| `__init__()` | 27-32 | Initialize manager | `api_key`, `project_name`, `endpoint` |
| `setup_environment()` | 45-51 | Configure env vars | `api_key`, `project_name`, `endpoint` |
| `create_prompt_template()` | 53-72 | Create versioned prompts | `template`, `handle`, `public` |
| `create_qa_chain()` | 74-97 | Build QA chains | `vectorstore`, `prompt_handle` |
| `evaluate_responses()` | 99-126 | Evaluate outputs | `predictions`, `references`, `criteria` |
| `create_monitored_chain()` | 128-147 | Create traced chains | `prompt_template` |

### Essential Usage Pattern
```python
# 1. Initialize
manager = LangSmithManager(api_key="...", project_name="...")

# 2. Create prompt
prompt = manager.create_prompt_template(template="...", handle="...")

# 3. Build chain
chain = manager.create_monitored_chain(prompt)

# 4. Run with tracing
result = chain.invoke({...})

# 5. Evaluate (optional)
eval_result = manager.evaluate_responses([result], [reference])
```

### File Navigation
- **Implementation**: [`src/Langsmith.py`](../src/Langsmith.py)
- **Core Class**: Lines 22-148
- **Usage Example**: Lines 150-188
- **Main Methods**: Lines 45-147

## Additional Resources
- [Official Documentation](https://docs.smith.langchain.com)
- [API Reference](https://api.smith.langchain.com/docs)
- [Example Projects](https://github.com/langchain-ai/langsmith-examples)
- [Community Forums](https://github.com/langchain-ai/langchain/discussions)