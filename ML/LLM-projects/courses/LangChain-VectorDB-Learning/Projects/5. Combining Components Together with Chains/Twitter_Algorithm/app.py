import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain

# Access the keys from the .env file
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ACTIVELOOP_TOKEN = os.getenv('ACTIVELOOP_TOKEN')

# Set the environment variables
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
os.environ['ACTIVELOOP_TOKEN'] = ACTIVELOOP_TOKEN

embeddings = OpenAIEmbeddings()

# Load all files inside the repository.
root_dir = './the-algorithm'
docs = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    for file in filenames:
        try: 
            loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
            docs.extend(loader.load_and_split())
        except Exception as e: 
            pass

# Divide the loaded files into chunks:
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)

# Check the content of the texts variable
print(f"Number of text chunks: {len(texts)}")

# Explicitly embed the texts using OpenAIEmbeddings
embedded_texts = [embeddings.embed(text) for text in texts]

# Perform the indexing process and upload embeddings to Deep Lake
db = DeepLake(dataset_path="hub://djpapzin/twitter-algorithm", embedding_function=embeddings)
db.add_documents(embedded_texts)  # Using the embedded texts

# Define the retriever
retriever = db.as_retriever()
retriever.search_kwargs['distance_metric'] = 'cos'
retriever.search_kwargs['fetch_k'] = 100
retriever.search_kwargs['maximal_marginal_relevance'] = True
retriever.search_kwargs['k'] = 10

# Load the dataset
db = DeepLake(dataset_path="hub://djpapzin/twitter-algorithm", read_only=True, embedding_function=embeddings)

# Connect to GPT-4 for question answering
model = ChatOpenAI(model='gpt-3.5-turbo')  # switch to 'gpt-4'
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

# Define questions and get answers
questions = [
    "What does favCountParams do?",
    "is it Likes + Bookmarks, or not clear from the code?",
    # ... [add more questions as needed]
] 
chat_history = []

for question in questions:  
    result = qa({"question": question, "chat_history": chat_history})
    chat_history.append((question, result['answer']))
    print(f"-> **Question**: {question} \n")
    print(f"**Answer**: {result['answer']} \n")
