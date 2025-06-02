# Self-Correction Agentic Retrieval Augment Generation

## What is this app?
This is an advanced Retrieval-Augmented Generation (RAG) application that utilizes multiple agents and a sophisticated workflow to provide accurate and context-aware responses to user queries based on documents or URLs provided by the user. The application combines document retrieval, web search, and language model generation to create a robust question-answering system. This can provide significant value in scenarios where the accuracy and relevance of information are critical, even with the trade-off in response time. Uses Ollama for model inference, langchain for agentic workflow and streamlit for simple user-interface.

### Demo
![Demo](/demo.gif)

## How to run (and deploy )?
* ### Local:
  1. Download, install and run ollama, please refer [this](https://github.com/ollama/ollama). Then, ```ollama pull llama3```
  2. Clone the repo: `git clone https://github.com/devgargd7/CorrectiveRAG.git` and `cd CorrectiveRAG`.
  3. Install the dependencies: `pip install -r requirements.txt`.
  4. Set up your variables in the application.yaml:
      - GOOGLE_CSE_ID
      - GOOGLE_API_KEY
      - ollama_url
      - OPENAI_API_KEY and OPENAI_ORGANIZATION (needed only for Evaluation)
  5. Run the app: `streamlit run app.py`
  6. (Optional) For **evaluation**: run `python evaluate.py`
* ### Deploy to Linux server (AWS) :
  1. Setup Ollama:
      - Required an EC2 instance `g4dn.xlarge` with Nvidia GPU and atleast 50 GB of storage, with ports `11434` open for inbound traffic.
      - Follow [this](https://github.com/varunvasudeva1/ollama-server-docs?tab=readme-ov-file#install-ollama) to install and run Ollama in this instance, if using llama3-8b, do ```ollama pull llama3```.
  2. Setup Application:
      - Follow steps 2-4 in Local.
      - Set up an ECR repository and add tags to the image in the `docker-compose.yaml`.
      - Build and push the image to the repository created above using `docker-compose build --no-cache` and  `docker-compose push`.
      - Spin up another EC2 instance (but with much lower configurations and ports 8501 and 8080 open for inbound traffic) and then, pull and build the image from ECR in this instance. May want to look at [this](https://medium.com/@sstarr1879/deploy-a-simple-dockerized-web-app-using-aws-ecr-ec2-e6a3569a6cf5).

### Requirements
  - Python: 3.8+
  - Ollama
  - Streamlit
  - LangChain
  - Google Custom Search API
  - Other dependencies listed in `requirements.txt`

### Configuration
- `application.yaml`: Contains configuration for the main application, including model names, API keys, and other settings.
- `prompts.yaml`: Stores prompt templates for various agents used in the application.

## Evaluation and Results
The `evaluate.py` script runs a separate evaluation of the RAG system using the RAGAS framework. It assesses the performance of different embedding models and the overall RAG chain using metrics such as context precision, context recall, faithfulness, and answer relevancy. The baseline RAG system is a simple RAG pipeline: `docs | prompt | llm | parse_output`

Metrics | This RAG    | Baseline RAG |
|------| -------- | ------- |
| Faithfulness | <span style="color:green">0.9139</span>  | 0.8730    |
| Answer Relevancy | <span style="color:green">0.7952</span> | 0.6624     |
| Avg Response Time (seconds) | <span style="color:red">26.207</span>    | 9.629    |

## Architecture/Workflow: 

![workflow](/arch.png)

- User Input: The user provides a uploads documents or URLs and then enter question through the Streamlit interface.
- Chain Routing: The application determines whether to use separate flow for Summary or simple QA.
- Document Retrieval: Relevant documents are retrieved from the vector store or web search. For vectore store, ChromaDb is used with embeddings using Ollama.
- Document Grading: Retrieved documents are evaluated for relevance to the question.
- Generation: An answer is generated using the relevant documents and the original question.
- Hallucination Grading: The generated answer is checked for hallucinations and relevance.
- Answer Grading: If necessary, the process repeats with web search or regeneration until a satisfactory answer is produced.

### Design decisions:
<details>
<summary> Why use Ollama on an EC2 (and not have Bedrock or VLLM)?</summary>
 - Langchain provides great support for Ollama from json formats for chat, which enable ease for such agentic workflows to providing API calls for embeddings. The performance (although not evaluated here) are similar with VLLM. And since, Ollama is also easy to install on many platform, it provides faster prototyping. Now, EC2 is being used here, as it provides more granular security which may be more crucial when uploading documents and making API calls to an LLM on a server, especially in industries like Financial orgs, Leagal, Medical Information Systems, etc.
</details>
<details>
<summary> Can we use serverless to deploy the RAG app?</summary>
Since, this application uses Streamlit for interfaces, it may not work on serverless as Streamlit depends on long running web sockets. But if the UI is replaces with API interface (like REST), serverless solutions can be used. 
</details>
<details>
<summary> Where can this system be used?</summary>
This RAG system demonstrates significant improvements in key areas of performance compared to the baseline, particularly in faithfulness and answer relevancy. However, it does come with a trade-off in response time. Thus, it can provide significant value in scenarios where the accuracy and relevance of information are critical.
</details>

### Potential Feature Roadmap:
- Multimodal Support
- Scalibilty (start with separating UI, RAG app, vector store DB using REST API designs)
- Responce time optimization (caching frequent queries/documents, hardware scaling)
