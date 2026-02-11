import json
import os
import pandas as pd
import magic  # for MIME detection
from pathlib import Path
import pdfplumber
from bs4 import BeautifulSoup





# Example function map based on extension or MIME
extension_func_map = {
    ".txt": "read_txt",
    ".pdf": "read_pdf",
    ".docx": "read_docx",
    ".doc": "read_doc",
    ".csv": "read_csv",
    ".xlsx": "read_xlsx",
    ".json": "read_json",
    ".md": "read_md",
    ".html": "read_html",
    ".pptx": "read_pptx",
   
  
}


mime_func_map = {
    "application/pdf": "read_pdf",
    "application/msword": "read_doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "read_docx",
    "text/plain": "read_txt",
    "application/json": "read_json",
    "text/html": "read_html",
 
}




# all files reads function

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def read_csv(path):
    df = pd.read_csv(path)
    return df.to_string(index=False)


def read_xlsx(path):
    df = pd.read_excel(path)
    return df.to_string(index=False)

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.dumps(json.load(f), indent=2)

def read_md(path):
    return read_txt(path)

def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    return soup.get_text()









# function to detect the documents extension and read the text
def detect_and_read(file_path):
    ext = Path(file_path).suffix.lower()

    if ext in extension_func_map:
        func_name = extension_func_map[ext]
    else:
        # fallback to MIME detection
        mime = magic.from_file(file_path, mime=True)
        func_name = mime_func_map.get(mime, None)

    if func_name:
        reader_func = globals().get(func_name)
        if reader_func:
            return reader_func(file_path)
        else:
            print(f"Function not implemented: {func_name}")
    else:
        print(f"Unsupported file format: {file_path}")
    return ""






# function to merge all files into one file
def get_file_contents(folder_path):
  
  """
  this function will take folder path of docs and read all documents and append in single file_contents.following file are supported ".txt" 
  ".pdf",".docx",".doc",".csv",".xlsx", ".json",".md",  ".html",  ".pptx"

  """
  file_contents = []
  
  for filename in os.listdir(folder_path):
      full_path = os.path.join(folder_path, filename)
      try:
          text = detect_and_read(full_path)
          if text:
              file_contents.append(text)
      except Exception as e:
          print(f"Error reading {filename}: {e}")

  return file_contents







