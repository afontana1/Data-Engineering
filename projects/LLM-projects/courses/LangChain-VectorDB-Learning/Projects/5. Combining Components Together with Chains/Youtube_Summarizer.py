import os
from dotenv import load_dotenv
import yt_dlp
import whisper
from langchain import OpenAI, LLMChain
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
import textwrap

# load API kets
load_dotenv() 

# set API keys
openai_api_key = os.environ['OPENAI_API_KEY']
activeloop_token = os.environ['ACTIVELOOP_TOKEN']

def download_mp4_from_youtube(url):
    # Set the options for the download
    filename = 'lecuninterview.mp4'
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': filename,
        'quiet': True,
    }

    # Download the video file
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)

url = "https://www.youtube.com/watch?v=mBjPyte2ZZo"
download_mp4_from_youtube(url)

# Whisper
model = whisper.load_model("base")
result = model.transcribe("lecuninterview.mp4")
print(result['text'])

with open ('text.txt', 'w') as file:  
    file.write(result['text'])
    

# Summarization with LangChain
llm = OpenAI(model_name="text-davinci-003", temperature=0)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"]
)

with open('text.txt') as f:
    text = f.read()

texts = text_splitter.split_text(text)
docs = [Document(page_content=t) for t in texts[:4]]

chain = load_summarize_chain(llm, chain_type="map_reduce")

output_summary = chain.run(docs)
wrapped_text = textwrap.fill(output_summary, width=100)
print(wrapped_text)

# The "stuff" approach
prompt_template = """Write a concise bullet point summary of the following:


{text}


CONSCISE SUMMARY IN BULLET POINTS:"""

BULLET_POINT_PROMPT = PromptTemplate(template=prompt_template, 
                        input_variables=["text"])


# nitialized the summarization chain using the stuff as chain_type and the prompt above.
chain = load_summarize_chain(llm, 
                             chain_type="stuff", 
                             prompt=BULLET_POINT_PROMPT)

output_summary = chain.run(docs)

wrapped_text = textwrap.fill(output_summary, 
                             width=1000,
                             break_long_words=False,
                             replace_whitespace=False)
print(wrapped_text)

# The 'refine' summarization chain is a method for generating more accurate and context-aware summaries.
# This method can result in more accurate and context-aware summaries compared to other chain types like 'stuff' and 'map_reduce'.
chain = load_summarize_chain(llm, chain_type="refine")

output_summary = chain.run(docs)
wrapped_text = textwrap.fill(output_summary, width=100)
print(wrapped_text)

