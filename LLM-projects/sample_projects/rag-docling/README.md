# 📚 Chat with Your Documents - Adaptive RAG System

> **Project Note**: This project was primarily developed using AI (Cursor AI) with minimal human code intervention. It was created as a self-imposed challenge to evaluate the current capabilities of AI coding assistants. While the AI was able to generate most of the functionality, success required prior technical knowledge to guide the model and fix simple bugs introduced by hallucinations. This experiment demonstrates both the potential and current limitations of AI-assisted development.

An advanced document interaction system built with Streamlit and LangChain, featuring adaptive RAG (Retrieval-Augmented Generation) capabilities for intelligent document processing and question answering.

## 🌟 Features

### Adaptive RAG Capabilities

- **Smart Source Selection**: Automatically routes queries between vectorstore and web search based on question type
- **Document Relevance Grading**: Evaluates retrieved documents for relevance and quality
- **Query Rewriting**: Automatically reformulates questions when initial retrievals are insufficient
- **Multi-Source Integration**: Combines results from local documents and web searches when needed

### Observability and Monitoring

- **LangSmith Integration**: Full observability into LLM chains and agents
- **Performance Tracking**: Monitor latency, token usage, and costs
- **Debug Traces**: Detailed traces for debugging and optimization
- **Quality Metrics**: Track relevance and accuracy of responses

### User Interface

- **Modern Chat Interface**: Clean, intuitive chat interface for natural interactions
- **Document Management**: Easy document upload and processing in the sidebar
- **Real-time Feedback**: Shows processing status and source information
- **Session Management**: Maintains chat history and document context

### Model Support

- **Multiple LLM Options**:
  - Claude 3.5 Sonnet: Best for complex tasks and deep analysis
  - Claude 3.5 Haiku: Fast responses while maintaining quality
  - GPT-4o: Advanced capabilities with multimodal support
  - GPT-4o Mini: Affordable and intelligent option

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- OpenAI API key (for embeddings and chat)
- Anthropic API key (optional, for Claude models)
- Tavily API key (for web search capabilities)
- LangSmith API key (for observability and monitoring)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/RAG_docling.git
cd RAG_docling
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
# Create .env file
touch .env

# Add your API keys
echo "OPENAI_API_KEY=your-openai-key" >> .env
echo "ANTHROPIC_API_KEY=your-anthropic-key" >> .env
echo "TAVILY_API_KEY=your-tavily-key" >> .env

# LangSmith Configuration
echo "LANGCHAIN_TRACING_V2=true" >> .env
echo "LANGCHAIN_ENDPOINT=https://api.smith.langchain.com" >> .env
echo "LANGCHAIN_API_KEY=your-langsmith-key" >> .env
echo "LANGCHAIN_PROJECT=docling-rag" >> .env
```

You can get your API keys from:

- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Tavily: https://tavily.com/
- LangSmith: https://smith.langchain.com/

### Running the App

```bash
streamlit run src/main.py
```

## 🔧 Configuration

### Model Configuration

- Models can be configured in `src/models/model_manager.py`
- Default settings optimize for accuracy while maintaining reasonable response times
- Temperature and other parameters can be adjusted for different use cases

### Document Processing

- Supports multiple document formats (PDF, TXT, DOCX)
- Configurable chunk size and overlap for document splitting
- Vector store settings can be adjusted in `src/models/vectorstore.py`

### Observability Settings

- LangSmith tracing is enabled by default for all LangChain components
- Project name can be customized in `.env` file
- Access traces and metrics at https://smith.langchain.com/
- Configure custom tags and metadata for better organization

## 🛠️ Architecture

### Core Components

- **Graph-based Processing**: Uses LangGraph for flexible query processing flow
- **Adaptive Routing**: Smart decision-making for source selection
- **Document Grading**: Quality assessment of retrieved information
- **Query Refinement**: Automatic question reformulation
- **Web Search**: Tavily integration for real-time information
- **Observability**: LangSmith integration for monitoring and debugging

### Data Flow

1. User uploads documents → processed into vector store
2. User asks question → routed to appropriate source (vectorstore or web search)
3. Documents retrieved → graded for relevance
4. If needed → question rewritten or additional sources consulted
5. Final answer generated → presented to user
6. All operations traced → monitored in LangSmith dashboard

## 📊 Monitoring and Analytics

### LangSmith Dashboard

- **Real-time Monitoring**: Track ongoing runs and system performance
- **Cost Analysis**: Monitor token usage and associated costs
- **Quality Metrics**: Evaluate response quality and relevance
- **Debug View**: Detailed traces for debugging and optimization
- **Custom Datasets**: Create and manage evaluation datasets
- **A/B Testing**: Compare different model configurations

### Performance Optimization

- Use LangSmith traces to identify bottlenecks
- Monitor token usage to optimize costs
- Track latency patterns for better user experience
- Analyze feedback for continuous improvement

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://python.langchain.com/)
- Uses [LangGraph](https://python.langchain.com/docs/langgraph) for flow control
- Vector storage by [Qdrant](https://qdrant.tech/)
- Web search by [Tavily](https://tavily.com/)
- Observability by [LangSmith](https://smith.langchain.com/)