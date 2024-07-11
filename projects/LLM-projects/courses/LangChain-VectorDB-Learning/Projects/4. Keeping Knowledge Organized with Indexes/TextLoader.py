from langchain.document_loaders import TextLoader

# Replace 'my_file.txt' with the actual path to the text file you want to load
loader = TextLoader('my_file.txt')

# Load the documents from the text file
documents = loader.load()

# You can print the documents to see the output
print(documents)
