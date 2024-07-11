import langchain
from langchain.document_loaders import ApifyDatasetLoader
from langchain.utilities import ApifyWrapper
from langchain.document_loaders.base import Document
import os

os.environ["APIFY_API_TOKEN"] = db.secrets.get("APIFY_API_TOKEN")

apify = ApifyWrapper()
loader = apify.call_actor(
    actor_id="apify/website-content-crawler", 
    run_input={"startUrls": [{"url": "djpapzin"}]},
    dataset_mapping_function=lambda dataset_item: Document(
        page_content=dataset_item["text"] if dataset_item["text"] else "No content available",
        metadata={
            "source": dataset_item["url"],
            "title": dataset_item["metadata"]["title"]
        }
    ),
)

docs = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

# we split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=20, length_function=len
)
docs_split = text_splitter.split_documents(docs)

from langchain.embeddings.cohere import CohereEmbeddings
from langchain.vectorstores import DeepLake
import os

os.environ["COHERE_API_KEY"] = db.secrets.get("COHERE_API_KEY")
os.environ["ACTIVELOOP_TOKEN"] = db.secrets.get("APIFY_API_TOKEN")

embeddings = CohereEmbeddings(model = "embed-english-v2.0")

username = "elleneal" # replace with your username from app.activeloop.ai
db_id = 'kb-material'# replace with your database name
DeepLake.force_delete_by_path(f"hub://{username}/{db_id}")

dbs = DeepLake(dataset_path=f"hub://{username}/{db_id}", embedding_function=embeddings)
dbs.add_documents(docs_split)

from langchain.vectorstores import DeepLake
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.retrievers import ContextualCompressionRetriever  
from langchain.retrievers.document_compressors import CohereRerank
import os

os.environ["COHERE_API_KEY"] = db.secrets.get("COHERE_API_KEY")
os.environ["ACTIVELOOP_TOKEN"] = db.secrets.get("ACTIVELOOP_TOKEN")

@st.cache_resource()
def data_lake():
    embeddings = CohereEmbeddings(model = "embed-english-v2.0")

    dbs = DeepLake(
        dataset_path="hub://elleneal/activeloop-material",
        read_only=True,
        embedding_function=embeddings
    )
    
    retriever = dbs.as_retriever()
    retriever.search_kwargs["distance_metric"] = "cos"
    retriever.search_kwargs["fetch_k"] = 20
    retriever.search_kwargs["maximal_marginal_relevance"] = True
    retriever.search_kwargs["k"] = 20

    compressor = CohereRerank(
        model = 'rerank-english-v2.0',
        top_n=5
    )
    
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )
    
    return dbs, compression_retriever, retriever

dbs, compression_retriever, retriever = data_lake()


from langchain.chat_tools import ConversationBufferWindowMemory

@st.cache_resource()
def memory():
    memory=ConversationBufferWindowMemory(
        k=3,
        memory_key="chat_history",
        return_messages=True, 
        output_key='answer'
    )
    return memory

memory=memory()


from langchain.chat_models import AzureChatOpenAI

BASE_URL = "<URL>"
API_KEY = db.secrets.get("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = "<deployment_name>"
llm = AzureChatOpenAI(
    openai_api_base=BASE_URL,
    openai_api_version="2023-03-15-preview",
    deployment_name=DEPLOYMENT_NAME,
    openai_api_key=API_KEY,
    openai_api_type="azure",
    streaming=True,
    verbose=True,
    temperature=0,
    max_tokens=1500,
    top_p=0.95
)

from langchain.chains import ConversationalRetrievalChain

qa = ConversationalRetrievalChain.from_llm(
    llm=llm, 
    retriever=compression_retriever, 
    memory=memory, 
    verbose=True, 
    chain_type="stuff", 
    return_source_documents=True
)

# UI code

if st.sidebar.button("Start a New Chat Interaction"):
    clear_cache_and_session()
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
def chat_ui(qa):

    if prompt := st.chat_input("Ask me questions: How can I retrieve data from Deep Lake in Langchain?"):
    
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            memory_variables = memory.load_memory_variables({})

            with st.spinner("Searching course material"):
                response = capture_and_display_output(
                    qa, ({"question": prompt, "chat_history": memory_variables})
                )

            full_response += response["answer"]
            message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

            source = response["source_documents"][0].metadata
            source2 = response["source_documents"][1].metadata
            with st.expander("See Resources"):
                st.write(f"Title: {source['title'].split('·')[0].strip()}")
                st.write(f"Source: {source['source']}")
                st.write(f"Relevance to Query: {source['relevance_score'] * 100}%")
                st.write(f"Title: {source2['title'].split('·')[0].strip()}")
                st.write(f"Source: {source2['source']}")
                st.write(f"Relevance to Query: {source2['relevance_score'] * 100}%")

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
        
chat_ui(qa)