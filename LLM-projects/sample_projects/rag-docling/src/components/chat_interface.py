import streamlit as st
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from graphs.chat_graph import process_question
import uuid

class ChatInterface:
    """Chat interface component for the Streamlit app."""
    
    def __init__(self):
        """Initialize chat interface."""
        # Initialize chat ID if not exists
        if "chat_id" not in st.session_state:
            st.session_state.chat_id = str(uuid.uuid4())
        
        # Initialize messages if not exists
        if "messages" not in st.session_state:
            st.session_state.messages = []
    
    def render(self):
        """Render the chat interface."""
        # Check if any documents are uploaded
        if not st.session_state.get("processed_files"):
            st.info("👋 Welcome! Please upload some documents using the sidebar before starting the chat.")
            return
        
        # Display chat messages from history
        for message in st.session_state.messages:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)
        
        # Accept user input
        if prompt := st.chat_input("Ask a question about your documents"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Add user message to chat history
            user_message = HumanMessage(content=prompt)
            st.session_state.messages.append(user_message)
            
            # Process the question and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        result = process_question(prompt)
                        response = result["generation"]
                        
                        # Display the response
                        st.markdown(response)
                        
                        # Add assistant message to chat history
                        assistant_message = AIMessage(content=response)
                        st.session_state.messages.append(assistant_message)
                    except Exception as e:
                        error_msg = f"An error occurred: {str(e)}"
                        st.error(error_msg)