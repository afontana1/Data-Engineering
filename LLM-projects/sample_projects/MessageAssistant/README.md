# MessageAssistantTool

---
Welcome to this (POC) project, where we delve into the integration of Semantic Chunking, Routing, and Prompt Agents. 
This application is a testament to functional Prompt design, to interact with domain-specific documents. 
By harnessing the synergy of these techniques, this application offers an efficient solution for searching 
and performing actions within a specific knowledge domain. In this case Public Relations and Communications industry. 

This project is broken down into two Phases broken down by semantic data ingestion and then semantic router driven prompting for more neuanced responce.

## Phase One

![phace1.png](statics/phace1.png)

---

- **Document Ingestion**: The `SrcIngestor` class is equipped to ingest files of various formats. It categorizes each file by type, processes its content, and stores the information in a designated 'memory bank' for future access.

- **File Processing**: Depending on the file type, I employ different methods to extract content and parsing it into text. Currently, it can only read PDFs and Images, extract textual content from images inside PDFs or standalone using Models capable of image processing, among others.

- **Text Analysis and Storage**: Instead of implementing a naive approach I use a [Semantic Chunking](https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/5_Levels_Of_Text_Splitting.ipynb) approach to break down text into related chunks, enhancing the efficiency of data retrieval.

- **PDF Processing (`preprocessor.py`)**: Currently this separate module specifically deals with PDF files, extracting text, images, and tables from each page. It also removes duplicate images and saves the processed content maintaining its original format.



## Phase Two

![phace2.png](statics/phace2.png)

---

- **Dynamic Interaction**: The code handles various types of questions, from straightforward definitions to requests for detailed explanations, adapting its responses based on previous interactions and the current user implied ask.

- **Content Routing**: Categorize questions to provide context-specific prompt, enhancing the relevance and accuracy of the models' inference.

- **Document Handling**: Interact with a LanceDB vector store, retrieving documents that are contextually relevant to the user's questions, ensuring that the responses are informed and precise.

- **Prompt Templating**: The system employs templated prompts to guide the language model's responses, ensuring that the information delivery is coherent, concise, and is able to navigate follow-up questions and new questions asked by the user.

## To Run it

This demo front end is written in streamlit which is a free and open-source framework to rapidly build and share machine learning and data science web apps. Make sure that you have your streamlit secrets updated with your API credentials.

Once you have downloaded all the dependencies all you need to run is the following command.

<code>
streamlit run \UntitledAssitantTool\main.py
</code>
