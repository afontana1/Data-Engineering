
from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("E:/Backup/Documents/Books/Sex Smart - Chapter 1.pdf")
pages = loader.load_and_split()

print(pages[0])