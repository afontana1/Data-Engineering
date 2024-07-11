import os
import re
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

class DeepLakeLoader:
    def __init__(self, source_data_path):
        self.source_data_path = source_data_path
        self.file_name = os.path.basename(source_data_path) # What we'll name our database
        self.data = self.split_data()
        
        if self.check_if_db_exists():
            self.db = self.load_db()
        else:
            self.db = self.create_db()

    def split_data(self):  # Correctly indented to be part of the class
        """  
        Preprocess the data by splitting it into passages.  

        If using a different data source, this function will need to be modified.  

        Returns:  
            split_data (list): List of passages.  
        """  
        with open(self.source_data_path, 'r') as f:  
            content = f.read()  
        split_data = re.split(r'(?=\d+\. )', content)
        if split_data[0] == '':  
            split_data.pop(0)  
        split_data = [entry for entry in split_data if len(entry) >= 30]  
        return split_data

    def load_db(self):  
        """  
        Load the database if it already exists.  

        Returns:  
            DeepLake: DeepLake object.  
        """  
        return DeepLake(dataset_path=f'deeplake/{self.file_name}', embedding_function=OpenAIEmbeddings(), read_only=True)  

    def create_db(self):  
        """  
        Create the database if it does not already exist.  

        Databases are stored in the deeplake directory.  

        Returns:  
            DeepLake: DeepLake object.  
        """  
        return DeepLake.from_texts(self.data, OpenAIEmbeddings(), dataset_path=f'deeplake/{self.file_name}')

    def query_db(self, query):  
        """  
        Query the database for passages that are similar to the query.  

        Args:  
            query (str): Query string.  

        Returns:  
            content (list): List of passages that are similar to the query.  
        """  
        results = self.db.similarity_search(query, k=3)  
        content = []
        for result in results:
            content.append(result.page_content)
        return content

    def check_if_db_exists(self):  # Placeholder for the missing method
        # You'll need to implement this method to check if the database exists
        pass

detected_objection = "Your query here"  # Define the query you want to use
db = DeepLakeLoader('salestesting.txt')
results = db.query_db(detected_objection)

objection_prompt = "Your prompt here"  # Define the prompt you want to use
chat = ChatOpenAI()
system_message = SystemMessage(content=objection_prompt)
human_message = HumanMessage(content=f'Customer objection: {detected_objection} | Relevant guidelines: {results}')

response = chat([system_message, human_message])
print(response.content)

