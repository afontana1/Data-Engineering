import streamlit as st
from utils.file_processor import process_file
from typing import List

class FileUploader:
    ALLOWED_TYPES = [
        "pdf", "txt", "docx", "pptx", "png", "jpg", "jpeg",
        "html", "htm", "md"
    ]
    
    def render(self):
        uploaded_files = st.file_uploader(
            "Upload your documents",
            accept_multiple_files=True,
            type=self.ALLOWED_TYPES,
            help="Supported formats: PDF, TXT, DOCX, PPTX, Images, HTML"
        )
        
        if uploaded_files:
            with st.spinner("Processing documents..."):
                for file in uploaded_files:
                    if file.name not in st.session_state.get("processed_files", []):
                        process_file(file)
                        if "processed_files" not in st.session_state:
                            st.session_state.processed_files = []
                        st.session_state.processed_files.append(file.name)
            
            st.success(f"✅ Processed {len(uploaded_files)} documents")
            # Show processed files
            if st.session_state.processed_files:
                with st.expander("📚 Processed Documents", expanded=False):
                    for file in st.session_state.processed_files:
                        st.write(f"- {file}")
        else:
            st.info("📄 Drag and drop your documents here or click to browse")