import os
import time

import nest_asyncio
import pandas as pd
from datasets import Dataset, load_dataset
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from ragas import RunConfig, evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    answer_relevancy,
    faithfulness,
)
from tqdm.auto import tqdm

from rag_app import App
from yaml_reader import YamlConfigReader

EVAL_EMBEDDING_MODELS = ["llama3"]
YAML_FILE_PATH = "application.yaml"

yaml_config_reader = YamlConfigReader(YAML_FILE_PATH)
os.environ["OPENAI_API_KEY"] = yaml_config_reader.get("OPENAI_API_KEY")
os.environ["OPENAI_ORGANIZATION"] = yaml_config_reader.get("OPENAI_ORGANIZATION")
eval_llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
eval_embd = OpenAIEmbeddings(model="text-embedding-3-small")

print("Evaluation: Loading Data")
data = load_dataset("explodinggradients/ragas-wikiqa", split="train")
df = pd.DataFrame(data)
print("Evaluation: Data Loaded")


class DocumentLoaderSplitter:
    def __init__(self, urls, pdf_file_paths, chunk_size=250, chunk_overlap=0):
        self.docs = urls
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def load_and_split_documents(self):
        docs_list = [item for sublist in self.docs for item in sublist]
        return self.text_splitter.create_documents(docs_list)


QUESTIONS = df["question"].to_list()
GROUND_TRUTH = df["correct_answer"].tolist()
CONTEXT = df["context"].tolist()

nest_asyncio.apply()

print("Evaluation: ----Embeddings----")
for model in EVAL_EMBEDDING_MODELS:
    data = {"question": [], "ground_truth": [], "contexts": []}
    data["question"] = QUESTIONS
    data["ground_truth"] = GROUND_TRUTH

    app = App(DocumentLoaderSplitter, model)
    print("Evaluation: App init")
    app.ingest(urls=CONTEXT)
    retriever = app.vector_store_retriever.get_retriever()
    print("Evaluation: Retriever init")
    # Getting relevant documents for the evaluation dataset
    for i in tqdm(range(0, len(QUESTIONS))):
        data["contexts"].append(
            [doc.page_content for doc in retriever.get_relevant_documents(QUESTIONS[i])]
        )
    # RAGAS expects a Dataset object
    print(data)
    dataset = Dataset.from_dict(data)
    # RAGAS runtime settings to avoid hitting OpenAI rate limits
    run_config = RunConfig(
        max_workers=4, max_wait=180, timeout=120, thread_timeout=200
    )  #
    print("Evaluation: Evaluating")
    result = evaluate(
        dataset=dataset,
        metrics=[context_precision, context_recall],
        run_config=run_config,
        llm=eval_llm,
        embeddings=eval_embd,
    )
    print(f"Result for the {model} model: {result}")


print("Evaluation: ----Baseline RAG Chain----")
app = App(DocumentLoaderSplitter)
print("Evaluation: App init")
app.ingest(urls=CONTEXT)
retriever = app.vector_store_retriever.get_retriever()
template = """Answer the question based only on the following context: \
{context}

Question: {question}
"""
# Defining the chat prompt
prompt = ChatPromptTemplate.from_template(template)
# Defining the model to be used for chat completion
# Naive RAG chain
rag_chain = (
    {
        "context": retriever
        | (lambda docs: "\n\n".join([d.page_content for d in docs])),
        "question": RunnablePassthrough(),
    }
    | prompt
    | ChatOllama(
        model=yaml_config_reader.get("model"),
        # format="json",
        temperature=0,
        timeout=5000,
    )
    | StrOutputParser()
)
print("Evaluation: App ingest")
start = time.time()
data = {"question": [], "ground_truth": [], "contexts": [], "answer": []}
data["question"] = QUESTIONS
data["ground_truth"] = GROUND_TRUTH
for i in tqdm(range(0, len(QUESTIONS))):
    question = QUESTIONS[i]
    data["answer"].append(rag_chain.invoke(question))
    data["contexts"].append(
        [doc.page_content for doc in retriever.get_relevant_documents(question)]
    )
end = time.time()
dataset = Dataset.from_dict(data)
print(data)
run_config = RunConfig(max_workers=4, max_wait=180)
print("Evaluation: Evaluating")
result = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy],
    run_config=run_config,
    raise_exceptions=False,
    llm=eval_llm,
    embeddings=eval_embd,
)
print(
    f"Result for the chain: {result}, average time elapsed: {(end-start)/len(QUESTIONS)}"
)


print("Evaluation: ----RAG Chain----")
data = {"question": [], "ground_truth": [], "contexts": [], "answer": []}
data["question"] = QUESTIONS
data["ground_truth"] = GROUND_TRUTH
# Using the best embedding model from the retriever evaluation
app = App(DocumentLoaderSplitter)
print("Evaluation: App init")
app.ingest(urls=CONTEXT)
retriever = app.vector_store_retriever.get_retriever()
print("Evaluation: App ingest")
elapseTime = []
for i in tqdm(range(0, len(QUESTIONS))):
    question = QUESTIONS[i]
    start = time.time()
    for output in app.invoke(question):
        for key, value in output.items():
            print(f"Finished running: {key}")
    data["answer"].append(value["generation"])
    end = time.time()
    print("Done:", i, "in", end - start)
    elapseTime.append(end - start)
    data["contexts"].append(
        [doc.page_content for doc in retriever.get_relevant_documents(question)]
    )

dataset = Dataset.from_dict(data)
run_config = RunConfig(max_workers=4, max_wait=180)
print("Evaluation: Evaluating")
result = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy],
    run_config=run_config,
    raise_exceptions=False,
    llm=eval_llm,
    embeddings=eval_embd,
)
print(
    f"Result for the chain: {result}, average time elapsed: {sum(elapseTime)/len(elapseTime)}"
)
