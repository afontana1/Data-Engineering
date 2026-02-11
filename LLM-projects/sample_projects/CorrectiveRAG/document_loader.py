from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores.utils import filter_complex_metadata


class DocumentLoaderSplitter:
    """
    Loads and splits documents from URLs or PDF files into chunks.

    Args:
        urls (list[str], optional): A list of URLs to load documents from.
        pdf_file_paths (list[str], optional): A list of paths to PDF files to load documents from.
            Exactly one of urls or pdf_file_paths must be provided.
        chunk_size (int, optional): The maximum size of each chunk. Defaults to 1000.
        chunk_overlap (int, optional): The number of characters to overlap between chunks. Defaults to 0.
    """

    def __init__(self, urls, pdf_file_paths, chunk_size=1000, chunk_overlap=0):
        self.paths = urls if not pdf_file_paths else pdf_file_paths
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.loader = WebBaseLoader if not pdf_file_paths else PyPDFLoader
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

    def load_and_split_documents(self):
        """
        Loads documents from URLs or PDF files and splits them into chunks.

        Returns:
            list: A list of documents, each with a page_content and metadata.
        """
        docs = [self.loader(path).load() for path in self.paths]
        docs_list = [item for sublist in docs for item in sublist]
        return filter_complex_metadata(self.text_splitter.split_documents(docs_list))
