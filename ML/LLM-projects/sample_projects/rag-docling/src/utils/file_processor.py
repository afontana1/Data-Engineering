from typing import BinaryIO, List, Dict, Any
from models.vectorstore import get_vectorstore
from utils.docling_processor import DoclingProcessor
import tempfile
import os
import logging
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_file(file: BinaryIO) -> None:
    """Process different file types and store them in the vector database."""
    
    # Create a temporary file to handle the uploaded file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.getvalue())
        file_path = tmp_file.name
        
        try:
            # Get file extension
            file_extension = file.name.split('.')[-1].lower()
            
            # Initialize Docling processor
            docling_processor = DoclingProcessor()
            
            # Process document with Docling
            try:
                # Extract text and context using Docling
                chunks = docling_processor.extract_text_with_context(file_path)
                
                # Prepare texts and metadata for vector store
                texts = []
                metadatas = []
                
                for chunk in chunks:
                    if chunk["text"].strip():
                        texts.append(chunk["text"])
                        metadatas.append({
                            "source": file.name,
                            "page": chunk["context"]["page_num"],
                            "section": chunk["context"]["header"],
                            "section_type": chunk["context"]["section_type"],
                            "has_tables": bool(chunk["context"]["tables"]),
                            "has_figures": bool(chunk["context"]["figures"]),
                            "has_images": bool(chunk["context"]["images"]),
                            "image_descriptions": [
                                img["analysis"] for img in chunk["context"]["images"]
                            ] if chunk["context"]["images"] else []
                        })
                
                # Store document structure in session state
                if "document_structures" not in st.session_state:
                    st.session_state.document_structures = {}
                
                # Get full document info for structure display
                doc_info = docling_processor.process_document(file_path)
                logger.info(f"Document info: {doc_info}")  # Log the full document info
                
                # Extract metadata with fallbacks
                metadata = doc_info.get("metadata", {})
                st.session_state.document_structures[file.name] = {
                    "title": metadata.get("title", "N/A"),
                    "author": metadata.get("author", "N/A"),
                    "date": metadata.get("date", "N/A"),
                    "num_pages": len(doc_info["pages"]),
                    "sections": [
                        {
                            "title": section.get("header"),
                            "page": section.get("page_number")
                        }
                        for section in doc_info.get("layout", {}).get("sections", [])
                        if section.get("header")
                    ],
                    "num_tables": len(doc_info.get("tables", [])),
                    "num_figures": len(doc_info.get("figures", [])),
                    "num_images": len(doc_info.get("images", [])),
                    "num_entities": len(doc_info.get("entities", [])),
                    "content": [
                        {
                            "page": page_num + 1,
                            "text": page.get("text", "") if isinstance(page, dict) else getattr(page, "text", "")
                        }
                        for page_num, page in enumerate(doc_info["pages"])
                    ]
                }
                
                logger.info(f"Document structure: {st.session_state.document_structures[file.name]}")
                
                # Store in vector database if we have valid texts
                if texts:
                    vectorstore = get_vectorstore()
                    logger.info(f"Adding {len(texts)} text chunks to vector store")
                    logger.info(f"Sample text: {texts[0][:200]}...")  # Log first 200 chars of first chunk
                    logger.info(f"Sample metadata: {metadatas[0]}")
                    vectorstore.add_texts(texts, metadatas=metadatas)
                    logger.info(f"Successfully processed {file.name} with Docling")
                else:
                    logger.warning(f"No valid text chunks extracted from {file.name}")
                
            except Exception as e:
                logger.error(f"Error processing {file.name} with Docling: {str(e)}")
                raise
            
        finally:
            # Clean up temporary file
            os.unlink(file_path)