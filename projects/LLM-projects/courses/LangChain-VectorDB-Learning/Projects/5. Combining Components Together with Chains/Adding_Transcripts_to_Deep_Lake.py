import os
from dotenv import load_dotenv
import yt_dlp
import whisper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.vectorstores import DeepLake
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

load_dotenv() 

openai_api_key = os.environ['OPENAI_API_KEY']
activeloop_token = os.environ['ACTIVELOOP_TOKEN']

def download_mp4_from_youtube(urls, job_id):
    # This will hold the titles and authors of each downloaded video
    video_info = []

    for i, url in enumerate(urls):
        # Set the options for the download
        file_temp = f'./{job_id}_{i}.mp4'
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': file_temp,
            'quiet': True,
        }

        # Download the video file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            title = result.get('title', "")
            author = result.get('uploader', "")

        # Add the title and author to our list
        video_info.append((file_temp, title, author))

    return video_info

urls=["https://www.youtube.com/watch?v=mBjPyte2ZZo&t=78s",
    "https://www.youtube.com/watch?v=cjs7QKJNVYM",]
video_details = download_mp4_from_youtube(urls, 1)

# load the model
model = whisper.load_model("base")

# iterate through each video and transcribe
results = []
for video in video_details:
    result = model.transcribe(video[0])
    results.append( result['text'] )
    print(f"Transcription for {video[0]}:\n{result['text']}\n")

with open ('text.txt', 'w') as file:  
    file.write(results['text'])
    
# Load the texts
with open('text.txt') as f:
    text = f.read()

# Split the documents
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"]
    )
texts = text_splitter.split_text(text)

# pack all the chunks into a Documents:
docs = [Document(page_content=t) for t in texts[:4]]

# import Deep Lake and build a database with embedded documents:
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')

# create Deep Lake dataset
# TODO: use your organization id here. (by default, org id is your username)
my_activeloop_org_id = "langchain_course_deeplake"
my_activeloop_dataset_name = "langchain_course_youtube_summarizer"
dataset_path = f"hub://{my_activeloop_org_id}/{my_activeloop_dataset_name}"

db = DeepLake(dataset_path=dataset_path, embedding_function=embeddings)
db.add_documents(docs)

# retrieve the information from the database,
# construct a retriever object.
retriever = db.as_retriever() #measures "distance" or similarity between different data points in the database. 
retriever.search_kwargs['distance_metric'] = 'cos' #use cosine similarity as its distance metric. used in information retrieval to measure the similarity between documents or pieces of text.
retriever.search_kwargs['k'] = 4 # return the 4 most similar or closest results according to the distance metric when a search is performed.

# RetrievalQA chain is useful to query similiar contents from databse and use the returned records as context to answer questions. 
prompt_template = """Use the following pieces of transcripts from a video to answer the question in bullet points and summarized. If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Summarized answer in bullter points:"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain_type_kwargs = {"prompt": PROMPT}
qa = RetrievalQA.from_chain_type(llm=llm,
                                 chain_type="stuff",
                                 retriever=retriever,
                                 chain_type_kwargs=chain_type_kwargs)

print( qa.run("Summarize the mentions of google according to their AI program") )