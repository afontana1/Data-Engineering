from datetime import datetime
import streamlit as st
import asyncio
import json
import uuid
import os

from langchain_core.messages import SystemMessage, AIMessage, HumanMessage   

from runnable import get_runnable

@st.cache_resource
def create_chatbot_instance():
    return get_runnable()

chatbot = create_chatbot_instance()

@st.cache_resource
def get_thread_id():
    return str(uuid.uuid4())

thread_id = get_thread_id()

system_message = f"""
You are a personal assistant who helps with research, managing Google Drive, and managing Slack. 
You never give IDs to the user since those are just for you to keep track of.
The link to any Google Doc is: https://docs.google.com/document/d/[document ID]
The current date is: {datetime.now().date()}
"""

async def prompt_ai(messages):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    async for event in chatbot.astream_events(
            {"messages": messages}, config, version="v2"
        ):
            if event["event"] == "on_chat_model_stream":
                yield event["data"]["chunk"].content            

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~ Main Function with UI Creation ~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

async def main():
    st.title("n8n LangChain Agent")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content=system_message)
        ]    

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        message_json = json.loads(message.json())
        message_type = message_json["type"]
        if message_type in ["human", "ai", "system"]:
            with st.chat_message(message_type):
                st.markdown(message_json["content"])        

    # React to user input
    if prompt := st.chat_input("What would you like to do today?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))

        # Display assistant response in chat message container
        response_content = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()  # Placeholder for updating the message
            # Run the async generator to fetch responses
            async for chunk in prompt_ai(st.session_state.messages):
                if isinstance(chunk, str):
                    response_content += chunk
                elif isinstance(chunk, list):
                    for chunk_text in chunk:
                        if "text" in chunk_text:
                            response_content += chunk_text["text"]
                else:
                    raise Exception("Chunk is not a string or list.")

                # Update the placeholder with the current response content
                message_placeholder.markdown(response_content)
        
        st.session_state.messages.append(AIMessage(content=response_content))


if __name__ == "__main__":
    asyncio.run(main())