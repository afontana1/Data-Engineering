from langchain.document_loaders import GoogleDriveLoader

loader = GoogleDriveLoader(
    folder_id="your_folder_id",
    recursive=False  # Optional: Fetch files from subfolders recursively. Defaults to False.
)

docs = loader.load()
