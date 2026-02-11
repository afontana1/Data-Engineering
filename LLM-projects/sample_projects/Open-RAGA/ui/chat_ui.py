import yaml
from pathlib import Path
import os

root_path = os.path.dirname(os.path.abspath(__file__))


# Load a .yaml or .yml file
with open(Path(root_path).parent/"config/dev/app_config.yaml", "r") as file:
    app_config = yaml.safe_load(file)


app_name = app_config['app_name']



import streamlit as st

st.title(f"{app_name}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})