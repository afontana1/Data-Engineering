# Research Rabbit 🐰

Research Rabbit is a web research and summarization assistant that autonomously goes down the rabbit-hole of any user-defined topic. It uses an LLM to generate a search query based on the user's topic, gets web search results, and uses an LLM to summarize the results. It then uses an LLM to reflect on the summary, examines knowledge gaps, and generates a new search query to fill the gaps. This repeats for a user-defined number of cycles, updating the summary with new information from web search and provided the user a final markdown summary with all sources used. It is configured to run with fully local LLMs (via [Ollama](https://ollama.com/search))! 

![research-rabbit](https://github.com/user-attachments/assets/4308ee9c-abf3-4abb-9d1e-83e7c2c3f187)

## 🚀 Quickstart

Pull a local LLM that you want to use from [Ollama](https://ollama.com/search):
```bash
ollama pull llama3.2
```

For free web search (up to 1000 requests), [you can use the Tavily API](https://tavily.com/):
```bash
export TAVILY_API_KEY=<your_tavily_api_key>
```

Clone the repository and launch the assistant with the LangGraph server:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/langchain-ai/research-rabbit.git
cd research-rabbit
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.11 langgraph dev
```

You should see the following output and Studio will open in your browser:
> Ready!
> 
> API: http://127.0.0.1:2024
> 
> Docs: http://127.0.0.1:2024/docs
> 
> LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024

Open `LangGraph Studio Web UI` via the URL in the output above. 

In the `configuration` tab:
* You can set the name of your local LLM to use with Ollama (it will by default be `llama3.2`) 
* You can set the depth of the research iterations (it will by default be `3`)

![Screenshot 2024-12-05 at 3 23 46 PM](https://github.com/user-attachments/assets/3c328426-b107-4ed5-82a5-625193f18435)

Give the assistant a topic for research, and you can visualize its process!

![Screenshot 2024-12-05 at 2 58 26 PM](https://github.com/user-attachments/assets/a409203b-60b7-41ee-9a6a-7defb3d520a7)

## How it works

Research Rabbit is a AI-powered research assistant that:
- Given a user-provided topic, uses a local LLM (via [Ollama](https://ollama.com/search)) to generate a web search query
- Uses a search engine (configured for [Tavily](https://www.tavily.com/)) to find relevant sources
- Uses a local LLM to summarize the findings from web search related to the user-provided research topic
- Then, it uses the local LLM to reflect on the summary, identifying knowledge gaps and generating a new search query to explore the gaps
- The process repeats, with the summary being iteratively updated with new information from web search
- It will repeat down the research rabbit hole 
- Runs for a configurable number of iterations (see `configuration` tab)  

This is inspired by [IterDRAG](https://arxiv.org/html/2410.04343v1#:~:text=To%20tackle%20this%20issue%2C%20we,used%20to%20generate%20intermediate%20answers.), which handles complex queries by decomposing the query into simpler sub-queries. This follows a sequential, interleaved process where each sub-query depends on the answer retrieved from the previous one, enabling dynamic query decomposition and adaptive retrieval.

## Outputs

The output of the graph is a markdown file containing the research summary, with citations to the sources used.

All sources gathered during research are saved to the graph state. 

You can visualize them in the graph state, which is visible in LangGraph Studio:

![Screenshot 2024-12-05 at 4 08 59 PM](https://github.com/user-attachments/assets/e8ac1c0b-9acb-4a75-8c15-4e677e92f6cb)

The final summary is saved to the graph state as well: 

![Screenshot 2024-12-05 at 4 10 11 PM](https://github.com/user-attachments/assets/f6d997d5-9de5-495f-8556-7d3891f6bc96)

## Deployment Options

There are [various ways](https://langchain-ai.github.io/langgraph/concepts/#deployment-options) to deploy this graph.

See [Module 6](https://github.com/langchain-ai/langchain-academy/tree/main/module-6) of LangChain Academy for a detailed walkthrough of deployment options with LangGraph.
